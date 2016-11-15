import luigi
import luigi.mock
import numpy as np
import pandas as pd
from sklearn import preprocessing

from clean_data import ImputeSchoolsMissingData, ImputeTeacherMissingData
from mapeamentos import dicionario_questoes_nomes_escola


class EncodeSchoolQuestions(luigi.Task):
    input_task = ImputeSchoolsMissingData()
    mappings = {'A': 3, 'B': 2, 'C': 1, 'D': 0}

    def requires(self):
        return self.input_task

    def output(self):
        return luigi.LocalTarget('./dados/2013/TS_ESCOLA_with_encoded_values.csv')

    def run(self):
        with self.input_task.output().open('r') as fp:
            escolas_2013_pd = pd.read_csv(fp)

        for col in escolas_2013_pd.filter(regex='TX_RESP_.*'):
            escolas_2013_pd[col].replace(to_replace=self.mappings, inplace=True)
        escolas_2013_pd.NIVEL_SOCIO_ECONOMICO.replace(to_replace={'Grupo {}'.format(i + 1): i + 1 for i in range(8)},
                                                      inplace=True)

        with self.output().open('w') as fp:
            escolas_2013_pd.to_csv(fp, index=False)


class EncodeTeacherQuestions(luigi.Task):
    input_task = ImputeTeacherMissingData()
    mappings = {'A': 0, 'B': 1, 'C': 2, 'D': 3, 'E': 4, 'F': 5, 'G': 6, 'H': 7, 'I': 8, 'J': 9, 'K': 10}

    def requires(self):
        return self.input_task

    def output(self):
        return luigi.LocalTarget('./dados/2013/TS_PROFESSOR_with_encoded_values.csv')

    def run(self):
        with self.input_task.output().open('r') as fp:
            professores_2013_pd = pd.read_csv(fp)

        for col in professores_2013_pd.filter(regex='TX_RESP_.*'):
            professores_2013_pd[col].replace(to_replace=self.mappings, inplace=True)

        with self.output().open('w') as fp:
            professores_2013_pd.to_csv(fp, index=False)


class ScaleFeatureValues(luigi.Task):
    def run(self):
        with self.input_task.output().open('r') as fp:
            dataset_pd = pd.read_csv(fp)

        processed_columns = self.get_columns_names(dataset_pd)

        dataset_pd.ix[:, processed_columns] = preprocessing.scale(dataset_pd[processed_columns])
        with self.output().open('w') as fp:
            dataset_pd.to_csv(fp, index=False)


class ScaleSchoolFeatureValues(ScaleFeatureValues):
    input_task = EncodeSchoolQuestions()

    def requires(self):
        return self.input_task

    def output(self):
        return luigi.LocalTarget('./dados/2013/TS_ESCOLA_with_scaled_values.csv')

    def get_columns_names(self, df):
        return np.append(df.filter(regex='TX_RESP_.*').columns.values, ['NIVEL_SOCIO_ECONOMICO'])


class ScaleTeacherFeatureValues(ScaleFeatureValues):
    input_task = EncodeTeacherQuestions()

    def requires(self):
        return self.input_task

    def output(self):
        return luigi.LocalTarget('./dados/2013/TS_PROFESSOR_with_scaled_values.csv')

    def get_columns_names(self, df):
        return df.filter(regex='TX_RESP_.*').columns.values


class RenameSchoolQuestionFeatures(luigi.Task):
    imputed_values_task = ScaleSchoolFeatureValues()

    def requires(self):
        return self.imputed_values_task

    def output(self):
        return luigi.LocalTarget('./dados/2013/TS_ESCOLA_with_renamed_features.csv')

    def run(self):
        with self.imputed_values_task.output().open('r') as fp:
            escolas_2013_pd = pd.read_csv(fp)

        with self.output().open('w') as fp:
            escolas_2013_pd.rename(columns=dicionario_questoes_nomes_escola).to_csv(fp, index=False)


class PersistModuleSchoolData(luigi.Task):
    input_task = RenameSchoolQuestionFeatures()

    def requires(self):
        return self.input_task

    def output(self):
        return luigi.LocalTarget('./dados/2013/TS_ESCOLA_preprocessed.csv')

    def run(self):
        with self.input_task.output().open('r') as fp:
            escolas_2013_pd = pd.read_csv(fp)

        with self.output().open('w') as fp:
            escolas_2013_pd.to_csv(fp, index=False)


class PersistModuleTeacherData(luigi.Task):
    input_task = ScaleTeacherFeatureValues()

    def requires(self):
        return self.input_task

    def output(self):
        return luigi.LocalTarget('./dados/2013/TS_PROFESSOR_preprocessed.csv')

    def run(self):
        with self.input_task.output().open('r') as fp:
            escolas_2013_pd = pd.read_csv(fp)

        with self.output().open('w') as fp:
            escolas_2013_pd.to_csv(fp, index=False)

import luigi
import luigi.mock
import pandas as pd
import numpy as np
from download_data import ExtractDataset


class DropLowAttendanceSchools(luigi.Task):
    extract_schools_task = ExtractDataset('TS_ESCOLA.csv')

    def requires(self):
        return self.extract_schools_task

    def output(self):
        return luigi.LocalTarget('./dados/2013/TS_ESCOLA_with_acceptable_attendance.csv')

    def run(self):
        with self.extract_schools_task.output().open('r') as fp:
            escolas_2013_pd = pd.read_csv(fp)
        escolas_2013_pd = escolas_2013_pd[escolas_2013_pd.TAXA_PARTICIPACAO_9EF > 0.5]

        with self.output().open('w') as fp:
            escolas_2013_pd.to_csv(fp, index=False)


class ImputeMissingData(luigi.Task):
    def run(self):
        with self.input_task.output().open('r') as fp:
            escolas_2013_pd = pd.read_csv(fp)

        imputed_values = {}
        for col in self.processed_columns_names(escolas_2013_pd):
            imputed_values[col] = escolas_2013_pd[col].value_counts().index[0]

        with self.output().open('w') as fp:
            escolas_2013_pd.fillna(value=imputed_values).to_csv(fp, index=False)


class ImputeSchoolsMissingData(ImputeMissingData):
    input_task = DropLowAttendanceSchools()

    def requires(self):
        return self.input_task

    def output(self):
        return luigi.LocalTarget('./dados/2013/TS_ESCOLA_with_imputed_values.csv')

    def processed_columns_names(self, df):
        return np.append(df.filter(regex='TX_RESP_Q.*').columns.values, ['NIVEL_SOCIO_ECONOMICO'])


class ImputeTeacherMissingData(ImputeMissingData):
    input_task = ExtractDataset('TS_PROFESSOR.csv')

    def requires(self):
        return self.input_task

    def output(self):
        return luigi.LocalTarget('./dados/2013/TS_PROFESSOR_with_imputed_values.csv')

    def processed_columns_names(self, df):
        return df.filter(regex='TX_RESP_Q.*').columns.values


class ImputeDirectorMissingData(ImputeMissingData):
    input_task = ExtractDataset('TS_DIRETOR.csv')

    def requires(self):
        return self.input_task

    def output(self):
        return luigi.LocalTarget('./dados/2013/TS_DIRETOR_with_imputed_values.csv')

    def processed_columns_names(self, df):
        return df.filter(regex='TX_RESP_Q.*').columns.values

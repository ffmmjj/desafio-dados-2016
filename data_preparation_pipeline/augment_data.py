import luigi
import numpy as np
import pandas as pd

from preprocess_data import ScaleDirectorFeatureValues, ScaleTeacherFeatureValues, \
    ScaleSchoolFeatureValues


class AppendTeacherAttendanceFeatureToSchool(luigi.Task):
    input_tasks = (ScaleSchoolFeatureValues(), ScaleDirectorFeatureValues())

    def requires(self):
        return self.input_tasks

    def output(self):
        return luigi.LocalTarget('./dados/2013/TS_ESCOLA_with_teacher_attendance.csv')

    def run(self):
        with self.input_tasks[0].output().open('r') as fp:
            escolas_pd = pd.read_csv(fp)
        with self.input_tasks[1].output().open('r') as fp:
            professores_pd = pd.read_csv(fp)

        escolas_indices = escolas_pd.ID_ESCOLA.isin(professores_pd.ID_ESCOLA)
        escolas_pd['TX_RESP_TEACHERS_ATTENDANCE'] = 0
        escolas_pd.ix[escolas_indices, 'TX_RESP_TEACHERS_ATTENDANCE'] = professores_pd.TX_RESP_Q073

        with self.output().open('w') as fp:
            escolas_pd.to_csv(fp, index=False)


class AppendFeaturesAggregatedFromTeachersDatasetToSchool(luigi.Task):
    input_tasks = (AppendTeacherAttendanceFeatureToSchool(), ScaleTeacherFeatureValues())

    def requires(self):
        return self.input_tasks

    def output(self):
        return luigi.LocalTarget('./dados/2013/TS_ESCOLA_with_teachers_features.csv')

    def impute_appended_values(self, dataset, columns):
        imputed_values = {}
        for col in columns:
            imputed_values[col] = dataset[col].value_counts().index[0]

        return dataset.fillna(value=imputed_values)

    def run(self):
        with self.input_tasks[0].output().open('r') as fp:
            escolas_pd = pd.read_csv(fp)
        with self.input_tasks[1].output().open('r') as fp:
            professores_pd = pd.read_csv(fp)

        questoes_ids = ['Q{}'.format(str(i).zfill(3)) for i in [8, 11, 12, 14, 57, 65, 103, 106]]
        questions = ['TX_RESP_{}'.format(q) for q in questoes_ids]
        professores_by_escola = professores_pd.filter(items=np.append(questions, 'ID_ESCOLA')).groupby('ID_ESCOLA')
        medians_by_escola = professores_by_escola.aggregate(np.median)

        escolas_pd = pd.merge(escolas_pd, medians_by_escola, left_on='ID_ESCOLA', right_index=True, how='left', suffixes=('', '_PROFESSOR'))

        with self.output().open('w') as fp:
            columns_to_impute = np.append(['{}_PROFESSOR'.format(q) for q in questions[0:6]], ['TX_RESP_Q103', 'TX_RESP_Q106'])
            self.impute_appended_values(escolas_pd, columns_to_impute).to_csv(fp, index=False)
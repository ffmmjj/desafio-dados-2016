import luigi
import pandas as pd
from preprocess_data import PersistModuleSchoolData, ScaleDirectorFeatureValues


class AppendTeacherAttendanceFeature(luigi.Task):
    input_tasks = (PersistModuleSchoolData(), ScaleDirectorFeatureValues())

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
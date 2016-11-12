import luigi
import pandas as pd
from sklearn.model_selection import train_test_split
from preprocess_data import PersistModuleTeacherData
from outliers_separation import SplitSchoolOutliersData


class SplitData(luigi.Task):
    def run(self):
        with self.get_input_file().open('r') as fp:
            dataset = pd.read_csv(fp)
        exploration_data, validation_data = train_test_split(dataset, train_size=0.75)
        exploration_df = pd.DataFrame(data=exploration_data, columns=dataset.columns)
        validation_df = pd.DataFrame(data=validation_data, columns=dataset.columns)

        task_outputs = self.output()
        with task_outputs['exploration'].open('w') as fp:
            exploration_df.to_csv(fp)
        with task_outputs['validation'].open('w') as fp:
            validation_df.to_csv(fp)


class SplitAvgSchoolData(SplitData):
    input_task = SplitSchoolOutliersData()

    def get_input_file(self):
        return self.input_task.output()['average']

    def requires(self):
        return self.input_task

    def output(self):
        return {'exploration': luigi.LocalTarget('./dados/2013/TS_ESCOLA_average_exploration_data.csv'),
                'validation': luigi.LocalTarget('./dados/2013/TS_ESCOLA_average_validation_data.csv')}


class SplitOutstandingSchoolData(SplitData):
    input_task = SplitSchoolOutliersData()

    def get_input_file(self):
        return self.input_task.output()['outstanding']

    def requires(self):
        return self.input_task

    def output(self):
        return {'exploration': luigi.LocalTarget('./dados/2013/TS_ESCOLA_outstanding_exploration_data.csv'),
                'validation': luigi.LocalTarget('./dados/2013/TS_ESCOLA_outstanding_validation_data.csv')}


class SplitTeachersData(SplitData):
    input_task = PersistModuleTeacherData()

    def get_input_file(self):
        return self.input_task.output()

    def requires(self):
        return self.input_task

    def output(self):
        return {'exploration':luigi.LocalTarget('./dados/2013/TS_PROFESSOR_exploration_data.csv'),
                'validation': luigi.LocalTarget('./dados/2013/TS_PROFESSOR_validation_data.csv')}
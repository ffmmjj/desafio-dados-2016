import luigi
import pandas as pd
from sklearn.model_selection import train_test_split
from preprocess_data import PersistModuleSchoolData, PersistModuleTeacherData


class SplitData(luigi.Task):
    def run(self):
        with self.input_task.output().open('r') as fp:
            dataset = pd.read_csv(fp)
        exploration_data, validation_data = train_test_split(dataset, train_size=0.75)
        exploration_df = pd.DataFrame(data=exploration_data, columns=dataset.columns)
        validation_df = pd.DataFrame(data=validation_data, columns=dataset.columns)

        task_outputs = self.output()
        with task_outputs[0].open('w') as fp:
            exploration_df.to_csv(fp)
        with task_outputs[1].open('w') as fp:
            validation_df.to_csv(fp)


class SplitSchoolData(SplitData):
    input_task = PersistModuleSchoolData()

    def requires(self):
        return self.input_task

    def output(self):
        return (luigi.LocalTarget('./dados/2013/TS_ESCOLA_exploration_data.csv'),
                luigi.LocalTarget('./dados/2013/TS_ESCOLA_validation_data.csv'))


class SplitTeachersData(SplitData):
    input_task = PersistModuleTeacherData()

    def requires(self):
        return self.input_task

    def output(self):
        return (luigi.LocalTarget('./dados/2013/TS_PROFESSOR_exploration_data.csv'),
                luigi.LocalTarget('./dados/2013/TS_PROFESSOR_validation_data.csv'))
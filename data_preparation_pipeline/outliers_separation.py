import luigi
import pandas as pd

from augment_data import AppendTeacherAttendanceFeature


class SplitSchoolOutliersData(luigi.Task):
    input_task = AppendTeacherAttendanceFeature()

    def requires(self):
        return self.input_task

    def output(self):
        return {'average': luigi.LocalTarget('./dados/2013/TS_ESCOLA_average.csv'),
                'outstanding': luigi.LocalTarget('./dados/2013/TS_ESCOLA_outstanding.csv')}

    def run(self):
        with self.input_task.output().open('r') as fp:
            escolas_pd = pd.read_csv(fp)

        escolas_statistics = escolas_pd['MEDIA_9EF_MT'].describe()
        math_avg, math_std = escolas_statistics.values[1], escolas_statistics.values[2]

        above_two_std_schools_indices = escolas_pd['MEDIA_9EF_MT'] > (math_avg + 2*math_std)
        below_two_std_schools_indices = escolas_pd['MEDIA_9EF_MT'] < (math_avg + 2*math_std)

        with self.output()['average'].open('w') as fp:
            escolas_pd[below_two_std_schools_indices].to_csv(fp)
        with self.output()['outstanding'].open('w') as fp:
            escolas_pd[above_two_std_schools_indices].to_csv(fp)
import luigi

from split_data import SplitTeachersData, SplitSchoolData


class AllDataTasks(luigi.Task):
    def requires(self):
        return SplitSchoolData(), SplitTeachersData()

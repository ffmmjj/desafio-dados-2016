import luigi

from split_data import SplitTeachersData, SplitAvgSchoolData, SplitOutstandingSchoolData


class AllDataTasks(luigi.WrapperTask):
    def requires(self):
        return SplitAvgSchoolData(), SplitOutstandingSchoolData(), SplitTeachersData()

import luigi

from partition_data import SplitTeachersData, SplitSchoolData
from preprocess_data import PersistModuleSchoolData, PersistModuleTeacherData


class AllDataTasks(luigi.Task):
    def requires(self):
        return SplitSchoolData(), SplitTeachersData()

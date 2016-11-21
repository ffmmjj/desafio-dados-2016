import luigi

from preprocess_data import ScaleDirectorFeatureValues, ScaleTeacherFeatureValues
from split_data import SplitAvgSchoolData, SplitOutstandingSchoolData


class AllDataTasks(luigi.WrapperTask):
    def requires(self):
        return SplitAvgSchoolData(), SplitOutstandingSchoolData(), ScaleTeacherFeatureValues(), ScaleDirectorFeatureValues()

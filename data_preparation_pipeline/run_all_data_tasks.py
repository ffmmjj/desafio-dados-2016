import luigi
from download_data import ExtractDataset
from preprocess_data import EncodeSchoolQuestions, ScaleFeatureValues

class AllDataTasks(luigi.Task):
	def requires(self):
		return (ScaleFeatureValues(), ExtractDataset('TS_PROFESSOR.csv'))

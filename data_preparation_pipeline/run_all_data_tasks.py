import luigi
from download_data import ExtractDataset
from preprocess_data import EncodeSchoolQuestions

class AllDataTasks(luigi.Task):
	def requires(self):
		return (EncodeSchoolQuestions(), ExtractDataset('TS_PROFESSOR.csv'))

import luigi
from download_data import ExtractDataset
from preprocess_data import PersistModuleData

class AllDataTasks(luigi.Task):
	def requires(self):
		return (PersistModuleData(), ExtractDataset('TS_PROFESSOR.csv'))

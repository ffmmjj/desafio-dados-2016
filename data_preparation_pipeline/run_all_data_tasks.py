import luigi
from download_data import ExtractDataset
from preprocess_data import PersistModuleSchoolData, PersistModuleTeacherData

class AllDataTasks(luigi.Task):
	def requires(self):
		return (PersistModuleSchoolData(), PersistModuleTeacherData())

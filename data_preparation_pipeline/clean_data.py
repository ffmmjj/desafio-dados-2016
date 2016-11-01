import luigi
import pandas as pd
from download_data import ExtractSchoolData


class DropLowAttendanceSchools(luigi.Task):
	extract_schools_task = ExtractSchoolData()

	def requires(self):
		return self.extract_schools_task

	def output(self):
		return luigi.LocalTarget(
				'../dados/2013/TS_ESCOLA_with_acceptable_attendance.csv',
				format=luigi.format.Nop
				)

	def run(self):
		escolas_2013_pd = pd.read_csv(self.extract_schools_task.output().path)
		escolas_2013_pd = escolas_2013_pd[escolas_2013_pd.TAXA_PARTICIPACAO_9EF > 0.5]

		escolas_2013_pd.to_csv(self.output().path, index=False)


class ImputeMissingData(luigi.Task):
	drop_low_attendance_schools_task = DropLowAttendanceSchools()

	def requires(self):
		return self.drop_low_attendance_schools_task

	def output(self):
		return luigi.LocalTarget(
				'../dados/2013/TS_ESCOLA_with_imputed_values.csv',
				format=luigi.format.Nop
				)

	def run(self):
		escolas_2013_pd = pd.read_csv(self.drop_low_attendance_schools_task.output().path)

		imputed_values = {}
		for col in escolas_2013_pd.filter(regex='TX_RESP_Q.*').columns:
			imputed_values[col] = escolas_2013_pd[col].value_counts().index[0]

		escolas_2013_pd.fillna(value=imputed_values).to_csv(self.output().path, index=False)
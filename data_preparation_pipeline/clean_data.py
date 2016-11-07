import luigi
import pandas as pd
from download_data import ExtractDataset
from src.carregamento.mapeamentos import dicionario_questoes_nomes_escola 


class DropLowAttendanceSchools(luigi.Task):
	extract_schools_task = ExtractDataset('TS_ESCOLA.csv')

	def requires(self):
		return self.extract_schools_task

	def output(self):
		return luigi.LocalTarget(
				'./dados/2013/TS_ESCOLA_with_acceptable_attendance.csv',
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
				'./dados/2013/TS_ESCOLA_with_imputed_values.csv',
				format=luigi.format.Nop
				)

	def run(self):
		escolas_2013_pd = pd.read_csv(self.drop_low_attendance_schools_task.output().path)

		imputed_values = {}
		for col in escolas_2013_pd.filter(regex='TX_RESP_Q.*').columns:
			imputed_values[col] = escolas_2013_pd[col].value_counts().index[0]
		imputed_values['NIVEL_SOCIO_ECONOMICO'] = escolas_2013_pd.NIVEL_SOCIO_ECONOMICO.value_counts().index[0]

		escolas_2013_pd.fillna(value=imputed_values).to_csv(self.output().path, index=False)


class RenameQuestionFeatures(luigi.Task):
	imputed_values_task = ImputeMissingData()

	def requires(self):
		return self.imputed_values_task

	def output(self):
		return luigi.LocalTarget(
				'./dados/2013/TS_ESCOLA_with_renamed_features.csv',
				format=luigi.format.Nop
				)

	def run(self):
		escolas_2013_pd = pd.read_csv(self.imputed_values_task.output().path)
		escolas_2013_pd.rename(columns=dicionario_questoes_nomes_escola).to_csv(self.output().path, index=False)

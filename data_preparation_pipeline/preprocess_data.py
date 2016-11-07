import luigi
import numpy as np
import pandas as pd
from sklearn import preprocessing
from clean_data import RenameQuestionFeatures


class EncodeSchoolQuestions(luigi.Task):
	input_task = RenameQuestionFeatures()
	mappings = {'A': 3, 'B': 2, 'C': 1, 'D': 0}

	def requires(self):
		return self.input_task

	def output(self):
		return luigi.LocalTarget(
				'./dados/2013/TS_ESCOLA_with_encoded_values.csv',
				format=luigi.format.Nop
				)

	def run(self):
		escolas_2013_pd = pd.read_csv(self.input_task.output().path)

		for col in escolas_2013_pd.filter(regex='Q_.*'):
			escolas_2013_pd[col].replace(to_replace=self.mappings, inplace=True)
		escolas_2013_pd.NIVEL_SOCIO_ECONOMICO.replace(to_replace={'Grupo {}'.format(i+1): i+1 for i in range(8)}, inplace=True)

		escolas_2013_pd.to_csv(self.output().path, index=False)


class ScaleFeatureValues(luigi.Task):
	input_task = EncodeSchoolQuestions()

	def requires(self):
		return self.input_task

	def output(self):
		return luigi.LocalTarget(
				'./dados/2013/TS_ESCOLA_with_scaled_values.csv',
				format=luigi.format.Nop
				)

	def run(self):
		escolas_2013_pd = pd.read_csv(self.input_task.output().path)
		processed_columns = np.append(escolas_2013_pd.filter(regex='Q_.*').columns.values, ['NIVEL_SOCIO_ECONOMICO'])

		escolas_2013_pd.ix[:, processed_columns] = preprocessing.scale(escolas_2013_pd[processed_columns])
		escolas_2013_pd.to_csv(self.output().path, index=False)

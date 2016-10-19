""" Data processing pipeline for Microdados Prova Brasil 2013 """

from tqdm import tqdm
import luigi
import requests
import zipfile


class Download2013Data(luigi.Task):
    owner_email = 'ffmmjj@gmail.com'

    def output(self):
        return luigi.LocalTarget(
            'dados/zipped_data/microdados_aneb_prova_brasil_2013.zip',
            format=luigi.format.Nop
            )

    def run(self):
        base_url = 'http://download.inep.gov.br/microdados/'
        response = requests.get(
            base_url + 'microdados_aneb_prova_brasil_2013.zip',
            stream=True
            )
        file_size = int(response.headers['content-length'])
        read_block_size = 512 * 1024

        with self.output().open('wb') as zipped_2013_data:
            with tqdm(total=file_size, desc='Downloading 2013 data') as pbar:
                for data in response.iter_content(chunk_size=read_block_size):
                    zipped_2013_data.write(data)
                    pbar.update(read_block_size)


class ExtractSchoolData(luigi.Task):
    def requires(self):
        return Download2013Data()

    def output(self):
        return luigi.LocalTarget(
            'dados/2013/TS_ESCOLA.csv',
            format=luigi.format.Nop
            )

    def run(self):
        zipped_file = zipfile.ZipFile(
            'dados/zipped_data/microdados_aneb_prova_brasil_2013.zip'
            )
        data = zipped_file.read('DADOS/TS_ESCOLA.csv')
        with self.output().open('wb') as school_data:
            school_data.write(data)

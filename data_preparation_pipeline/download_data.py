import zipfile

import luigi
import requests
from tqdm import tqdm


class Download2013Data(luigi.Task):
    def output(self):
        return luigi.LocalTarget(
            './dados/zipped_data/microdados_aneb_prova_brasil_2013.zip',
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


class ExtractDataset(luigi.Task):
    dataset_name = luigi.Parameter()

    def requires(self):
        return Download2013Data()

    def output(self):
        return luigi.LocalTarget(
            './dados/2013/{}'.format(self.dataset_name),
            format=luigi.format.Nop
            )

    def run(self):
        zipped_file = zipfile.ZipFile(
            './dados/zipped_data/microdados_aneb_prova_brasil_2013.zip'
            )
        data = zipped_file.read('DADOS/{}'.format(self.dataset_name))
        with self.output().open('wb') as dataset:
            dataset.write(data)

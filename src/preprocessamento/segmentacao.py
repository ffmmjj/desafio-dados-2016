from src.carregamento.preprocessamento_escola_2013 import escolas_2013_pd
from src.preprocessamento import codificacao


_NSE = 'NIVEL_SOCIO_ECONOMICO'

escolas_2013_codificada_pd = codificacao.codificar_questoes(escolas_2013_pd)

indices_se_baixo = (escolas_2013_codificada_pd[_NSE] == 'Grupo 1') | (escolas_2013_codificada_pd[_NSE] == 'Grupo 2')
indices_se_medio = (escolas_2013_codificada_pd[_NSE] == 'Grupo 3') | (escolas_2013_codificada_pd[_NSE] == 'Grupo 4') | (escolas_2013_codificada_pd[_NSE] == 'Grupo 5')
indices_se_alto = (escolas_2013_codificada_pd[_NSE] == 'Grupo 6') | (escolas_2013_codificada_pd[_NSE] == 'Grupo 7')

escolas_2013_codificada_pd['ID_SOCIOECONOMICO_BAIXO'] = 0
escolas_2013_codificada_pd.loc[indices_se_baixo, ['ID_SOCIOECONOMICO_BAIXO']] = 1
escolas_2013_codificada_pd['ID_SOCIOECONOMICO_MEDIO'] = 0
escolas_2013_codificada_pd.loc[indices_se_medio, ['ID_SOCIOECONOMICO_MEDIO']] = 1
escolas_2013_codificada_pd['ID_SOCIOECONOMICO_ALTO'] = 0
escolas_2013_codificada_pd.loc[indices_se_alto, ['ID_SOCIOECONOMICO_ALTO']] = 1

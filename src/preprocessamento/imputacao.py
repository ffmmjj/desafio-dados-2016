from src.preprocessamento.segmentacao import escolas_2013_codificada_pd
from src.carregamento.mapeamentos import nomes_questoes_escolas_2013

escolas_2013_codificada_pd = escolas_2013_codificada_pd[escolas_2013_codificada_pd['NIVEL_SOCIO_ECONOMICO'].notnull()]

indices_baixo = escolas_2013_codificada_pd['ID_SOCIOECONOMICO_BAIXO'] == 1
indices_medio = escolas_2013_codificada_pd['ID_SOCIOECONOMICO_MEDIO'] == 1
indices_alto = escolas_2013_codificada_pd['ID_SOCIOECONOMICO_ALTO'] == 1
escolas_nse_baixo = escolas_2013_codificada_pd[indices_baixo]
escolas_nse_medio = escolas_2013_codificada_pd[indices_medio]
escolas_nse_alto = escolas_2013_codificada_pd[indices_alto]

medians_baixo = escolas_nse_baixo.median()
medians_medio = escolas_nse_medio.median()
medians_alto = escolas_nse_alto.median()

nomes_questoes_escolas_2013.extend(['MEDIA_9EF_MT', 'MEDIA_9EF_LP'])

for q in nomes_questoes_escolas_2013:
    escolas_2013_codificada_pd.loc[indices_baixo, q] = escolas_2013_codificada_pd[indices_baixo][q].fillna(medians_baixo[q])
    escolas_2013_codificada_pd.loc[indices_medio, q] = escolas_2013_codificada_pd[indices_medio][q].fillna(medians_medio[q])
    escolas_2013_codificada_pd.loc[indices_alto, q] = escolas_2013_codificada_pd[indices_alto][q].fillna(medians_alto[q])

escolas_nse_baixo = escolas_2013_codificada_pd[indices_baixo]
escolas_nse_medio = escolas_2013_codificada_pd[indices_medio]
escolas_nse_alto = escolas_2013_codificada_pd[indices_alto]

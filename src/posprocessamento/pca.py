from src.carregamento.preprocessamento_escola_2013 import escolas_2013_pd
from src.preprocessamento import codificacao
from sklearn.decomposition import PCA


escolas_2013_codificada_pd = codificacao.codificar_questoes(escolas_2013_pd)
colunas_questoes = escolas_2013_codificada_pd.filter(regex='(Q_INFRA|Q_RECURSOS|Q_BIBLIOTECA).*').columns.values

escolas_2013_pca_values = escolas_2013_codificada_pd[colunas_questoes]
fitted_pca = PCA(n_components=2).fit(escolas_2013_pca_values)
escolas_2013_pos_pca = fitted_pca.transform(escolas_2013_pca_values)
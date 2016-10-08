import pandas as pd
import numpy as np
from sklearn.cross_validation import train_test_split


def questoes_ids():
    questao_base = 'TX_RESP_Q{}'
    for i in range(1, 67):
        yield questao_base.format(str(i).zfill(3))

resultados_escola_pd = pd.read_csv('../dados/prova_brasil_2011/TS_RESULTADO_ESCOLA.csv', delimiter=';')
questionario_escola_pd = pd.read_csv('../dados/prova_brasil_2011/TS_QUEST_ESCOLA.csv', delimiter=';')
join_columns = ['ID_PROVA_BRASIL', 'ID_UF', 'ID_MUNICIPIO', 'ID_DEPENDENCIA_ADM', 'ID_LOCALIZACAO', 'ID_ESCOLA']
escolas_info_pd = pd.merge(questionario_escola_pd, resultados_escola_pd, on=join_columns, how='outer')

nomes_features = [
    'Q_INFRA_TELHADO',
    'Q_INFRA_PAREDES',
    'Q_INFRA_PISO',
    'Q_INFRA_ENTRADA_PREDIO',
    'Q_INFRA_PATIO',
    'Q_INFRA_CORREDORES',
    'Q_INFRA_SALAS_DE_AULA',
    'Q_INFRA_PORTAS',
    'Q_INFRA_JANELAS',
    'Q_INFRA_BANHEIROS',
    'Q_INFRA_COZINHA',
    'Q_INFRA_INSTALACOES_HIDRAULICAS',
    'Q_INFRA_INSTALACOES_ELETRICAS',
    'Q_INFRA_SALAS_ILUMINADAS',
    'Q_INFRA_SALAS_AREJADAS',
    'Q_SEGURANCA_MUROS',
    'Q_SEGURANCA_ENTRADA_SAIDA_ALUNOS',
    'Q_SEGURANCA_ENTRADA_SAIDA_ESTRANHOS',
    'Q_SEGURANCA_PORTOES_TRANCADOS_DURANTE_AULA',
    'Q_SEGURANCA_VIGILANCIA_DIURNO',
    'Q_SEGURANCA_VIGILANCIA_NOTURNO',
    'Q_SEGURANCA_VIGILANCIA_FIM_DE_SEMANA',
    'Q_SEGURANCA_POLICIAMENTO_FURTOS_E_ROUBOS',
    'Q_SEGURANCA_POLICIAMENTO_DROGAS_DENTRO_DA_ESCOLA',
    'Q_SEGURANCA_POLICIAMENTO_DROGAS_FORA_DA_ESCOLA',
    'Q_SEGURANCA_PROTECAO_INCENDIO',
    'Q_SEGURANCA_SALA_EQUIPAMENTOS_TRANCADA',
    'Q_SEGURANCA_SINAIS_DEPREDACAO',
    'Q_SEGURANCA_BOA_ILUMINACAO_FORA_DA_ESCOLA',
    'Q_SEGURANCA_PROTECAO_ALUNOS_FORA_DA_ESCOLA',
    'Q_RECURSOS_COMPUTADORES_PARA_ALUNOS',
    'Q_RECURSOS_INTERNET_PARA_ALUNOS',
    'Q_RECURSOS_COMPUTADORES_PARA_PROFESSORES',
    'Q_RECURSOS_INTERNET_PARA_PROFESSORES',
    'Q_RECURSOS_COMPUTADORES_ADMINISTRACAO',
    'Q_RECURSOS_VIDEOS_EDUCATIVOS',
    'Q_RECURSOS_VIDEOS_LAZER',
    'Q_RECURSOS_COPIADORA',
    'Q_RECURSOS_IMPRESSORA',
    'Q_RECURSOS_RETROPROJETOR',
    'Q_RECURSOS_PROJETOR_SLIDES',
    'Q_RECURSOS_CASSETE_OU_DVD',
    'Q_RECURSOS_TELEVISAO',
    'Q_RECURSOS_MIMEOGRAFO',
    'Q_RECURSOS_CAMERA',
    'Q_RECURSOS_ANTENA_PARABOLICA',
    'Q_RECURSOS_LINHA_TELEFONICA',
    'Q_RECURSOS_APARELHOS_DE_FAX',
    'Q_RECURSOS_APARELHO_DE_SOM',
    'Q_RECURSOS_BIBLIOTECA',
    'Q_RECURSOS_QUADRA_ESPORTIVA',
    'Q_RECURSOS_LABORATORIO',
    'Q_RECURSOS_AUDITORIO',
    'Q_RECURSOS_SALA_DE_MUSICA',
    'Q_RECURSOS_SALA_DE_ARTES_PLASTICAS',
    'Q_RECURSOS_SALA_DE_LEITURA',
    'Q_BIBLIOTECA_ACERVO_DIVERSIFICADO',
    'Q_BIBLIOTECA_BRINQUEDOTECA',
    'Q_BIBLIOTECA_ESPACO_DE_ESTUDOS_COLETIVO',
    'Q_BIBLIOTECA_LIVROS_PODEM_SER_EMPRESTADOS',
    'Q_BIBLIOTECA_ABERTA_A_COMUNIDADE',
    'Q_BIBLIOTECA_ESPACO_AREJADO_E_ILUMINADO',
    'Q_BIBLIOTECA_PESSOA_NO_ATENDIMENTO',
    'Q_BIBLIOTECA_ALUNOS_PODEM_LEVAR_LIVROS',
    'Q_BIBLIOTECA_PROFESSORES_PODEM_LEVAR_LIVROS',
    'Q_BIBLIOTECA_COMUNIDADE_PODE_LEVAR_LIVROS'
]
dicionario_questoes_nomes_escola = {
    questao_id: nomes_features[index] for (index, questao_id) in enumerate(questoes_ids())
}
escolas_info_pd.rename(columns=dicionario_questoes_nomes_escola, inplace=True)
columns = np.asarray(escolas_info_pd.drop(['MEDIA_LP', 'MEDIA_MT'], 1).columns.values)

train_df, test_df, train_df_target, test_df_target = train_test_split(escolas_info_pd[columns], escolas_info_pd[['MEDIA_MT', 'MEDIA_LP']], test_size=0.25, random_state=0)
escolas_info_train = pd.DataFrame(data=np.hstack((train_df, train_df_target)), columns=np.append(columns, ['MEDIA_MT', 'MEDIA_LP']))
escolas_info_test = pd.DataFrame(data=np.hstack((test_df, test_df_target)), columns=np.append(columns, ['MEDIA_MT', 'MEDIA_LP']))

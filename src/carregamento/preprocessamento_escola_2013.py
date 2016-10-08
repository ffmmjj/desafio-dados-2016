import pandas as pd

from src.carregamento.mapeamentos import dicionario_questoes_nomes_escola


def remove_nao_preenchidos(df):
    return df[df['IN_PREENCHIMENTO_QUESTIONARIO'] == 1]


def filter_questoes_infra(df):
    return df.filter(regex='Q_INFRA.*')


def filter_questoes_recursos(df):
    return df.filter(regex='Q_RECURSOS.*')


def impute_missing_values(df, column):
    pass

_escolas_2013_raw_pd = remove_nao_preenchidos(
    pd.read_csv(
        '../dados/prova_brasil_2013/TS_ESCOLA.csv'
    ).rename(
        columns=dicionario_questoes_nomes_escola
    )
)
_escolas_2013_raw_preenchido_pd = _escolas_2013_raw_pd[_escolas_2013_raw_pd['IN_PREENCHIMENTO_QUESTIONARIO'] == 1]
_escolas_2013_raw_publicas_pd = _escolas_2013_raw_preenchido_pd[_escolas_2013_raw_preenchido_pd['ID_DEPENDENCIA_ADM'] != 4]
_escolas_2013_raw_publicas_nao_federais = _escolas_2013_raw_publicas_pd[_escolas_2013_raw_publicas_pd['ID_DEPENDENCIA_ADM'] != 1]

escolas_2013_pd = _escolas_2013_raw_publicas_nao_federais

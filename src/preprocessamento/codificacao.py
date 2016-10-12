
def codificar_questoes(questionario_pd):
    questionario_tratado_pd = questionario_pd.copy()
    for questoes in questionario_tratado_pd.filter(regex='Q_.*').columns:
        questionario_tratado_pd[questoes] = questionario_pd[questoes].map({'A': 3, 'B': 2, 'C': 1, 'D': 0}).fillna(0)

    return questionario_tratado_pd

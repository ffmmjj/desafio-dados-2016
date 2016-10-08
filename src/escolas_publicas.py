from src.carregamento.preprocessamento_escola_2011 import escolas_info_train

escolas_publicas_nao_federais = escolas_info_train[escolas_info_train['ID_DEPENDENCIA_ADM'] != 1]

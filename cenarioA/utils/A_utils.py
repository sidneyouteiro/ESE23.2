import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd


def dist_cumulativa(data, sem_outliers=False):
    fig, axs = plt.subplots(ncols=3,nrows=1)
    fig.set_figheight(5)
    fig.set_figwidth(15)
    c_d = 'Tempo Inspeçao (horas)'
    
    for i,j in zip(['Pequeno','Médio','Grande'],axs.flat):
        projetos_mesmo_porte = data.loc[data['Porte'] == i].copy()

        if sem_outliers:
            p_m_p_tecnica_group = projetos_mesmo_porte.groupby(by=['Técnica'])
            projetos_mesmo_porte = pd.concat([remocao_todos_outliers(j,c_d) for _, j in p_m_p_tecnica_group])
        
        sns.histplot(data=projetos_mesmo_porte,x=c_d,cumulative=True,hue='Técnica',
                     hue_order=['ACME','AXADEFEITO'],ax=j)
        j.set_title(f'Histograma cumulativo - {i}')
        j.set_ylabel('# Projetos')
    fig.suptitle('Histogramas sem outliers' if sem_outliers else 'Histogramas com outliers')
    plt.show()

def plot_boxplot(data,colunas_de_interesse):
    fig, axs = plt.subplots(ncols=3,nrows=1)
    fig.set_figheight(5)
    fig.set_figwidth(15)
    for i,j in zip(colunas_de_interesse,axs.flat):
        sns.boxplot(data=data,x='Porte',y=i,ax=j,hue='Técnica')
    plt.show()

def teste_shapiro(groups,colunas_de_interesse):
    from scipy.stats import shapiro

    idx_list = [i for i,_ in groups]
    dict_tests = {i+'-Shapiro':[] for i in colunas_de_interesse}
    for name, group in groups:
        for coluna in colunas_de_interesse:
            dict_tests[coluna+'-Shapiro'].append(shapiro(group[coluna]))

    return idx_list, dict_tests
def avaliacao_teste_shapiro(idx_list,dict_tests,alfa=0.05):
    indexs = pd.MultiIndex.from_tuples(idx_list)
    df_result = pd.DataFrame(dict_tests, index=indexs)
    for i in dict_tests.keys():
        df_result[i+'Resultado'] = df_result[i].map(lambda x: 'Normal' if x[1] < alfa else 'Sem evidência para rejeitar H0')
    return df_result

def teste_levene(projetos_utilizaveis,coluna='Tempo Inspeçao (horas)'):
    from scipy.stats import levene

    tecnica_porte_group = projetos_utilizaveis.groupby(by=['Técnica','Porte'])
    porte_tecnica_group = projetos_utilizaveis.groupby(by=['Porte','Técnica'])

    levene_dict = {}
    for (idx1,a),(idx2,b),(idx3,c) in agrupar(tecnica_porte_group,n=3):
        levene_dict[idx1[0]] = levene(a[coluna], b[coluna], c[coluna])

    for (idx1,a),(idx2,b) in agrupar(porte_tecnica_group):
        levene_dict[idx1[0]] = levene(a[coluna],b[coluna])
    return levene_dict
    
def teste_mannwhitneyu(group, colunas_de_interesse):
    from scipy.stats import mannwhitneyu

    result = {i:[] for i in colunas_de_interesse}
    for (idx1,acme_sample),(idx2,axa_sample) in agrupar(group):
        for coluna in colunas_de_interesse:
            result[coluna].append(mannwhitneyu(acme_sample[coluna],axa_sample[coluna]))

    return pd.DataFrame(result, index=['Grande','Médio','Pequeno'])

def agrupar(x, n=2):
    return zip(*[iter(x)]*n)

def remocao_todos_outliers(df,coluna):
    Q1 = df[coluna].quantile(0.25)
    Q3 = df[coluna].quantile(0.75)
    IQR = Q3 - Q1
    maximum, minimum = Q3+1.5*IQR, Q1-1.5*IQR
    dados_sem_outliers = df.loc[(df[coluna]<=maximum)&(df[coluna]>=minimum)].copy()
    return dados_sem_outliers
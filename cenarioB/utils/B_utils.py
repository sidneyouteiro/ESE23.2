import seaborn as sns
import matplotlib.pyplot as plt

def agrupar(x, n=2):
    return zip(*[iter(x)]*n)

def plot_boxplot(data,colunas_de_interesse): 
    fig, axs = plt.subplots(ncols=3,nrows=2,squeeze=False)
    
    axs[1][2].set_visible(False)

    for i,j in zip(axs[0],range(3)):
        i.set_position([0.07+j*0.31,0.525,0.228,0.343])
    axs[1][0].set_position([0.24,0.075,0.228,0.343])
    axs[1][1].set_position([0.55,0.075,0.228,0.343])

    fig.set_figheight(7)
    fig.set_figwidth(12)

    flat_axs = [i for i in axs.flat]
    for i,j in zip(colunas_de_interesse, flat_axs[:-1]):
        sns.boxplot(data=data,x='Porte',y=i,ax=j,hue='SUCESSO')

    Line, Label = flat_axs[0].get_legend_handles_labels()
    fig.legend(Line,Label, loc='lower left',title='O projeto foi um sucesso?',title_fontproperties={'weight':'bold'})
    lines, labels = [], []
    for ax in flat_axs[:-1]:
        ax.get_legend().remove()

    plt.show()
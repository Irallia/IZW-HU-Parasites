import matplotlib.cbook as cbook
import matplotlib.pyplot as plt
import numpy as np
from matplotlib.ticker import NullFormatter  # useful for `logit` scale

def main():
    unknown10 = '10-unknown_plot'
    unknown20 = '20-unknown_plot'
    unknown30 = '30-unknown_plot'
    unknown40 = '40-unknown_plot'
    unknown50 = '50-unknown_plot'


    # plt.figure(1)
    f, axs = plt.subplots(2,2,figsize=(9, 5))
    plt.suptitle('Influence of unknown data to prediction', fontsize=12, y=1)

    plot_data(231, unknown10)
    plot_data(232, unknown20)
    plot_data(233, unknown30)
    plot_data(234, unknown40)
    plot_data(235, unknown50)

    plt.tight_layout()
    plt.show()
    return

def plot_data(nr, datafile):
    filepath = 'evaluation/' + datafile + '.csv'
    data = np.genfromtxt(filepath, delimiter=',', skip_header=1, skip_footer=0, names=['unknown', 'y_fitch', 'y_my', 'y_sankoff'])

    plt.subplot(nr)
    plt.title(datafile)
    # ax1.set_title('Influence of unknown data to prediction')
    plt.xlabel('percentage unknown')
    plt.ylabel('correct predicted')
    plt.plot(data['unknown'], data['y_fitch'], color='g', linestyle='dashed', 
        label='Fitch', linewidth=0.5, marker='.', markerfacecolor='black')#, markersize=5)
    plt.plot(data['unknown'], data['y_my'], color='m', linestyle='dashed', 
        label='My', linewidth=0.5, marker='.', markerfacecolor='black')
    plt.plot(data['unknown'], data['y_sankoff'], color='c', linestyle='dashed', 
        label='Sankoff', linewidth=0.5, marker='.', markerfacecolor='black')
    plt.legend(loc="upper right") #, scatterpoints=1, numpoints=2)
    plt.axis([0, 1, 50, 100])
    # ax1.set_yscale('log')
    # ax1.set_yscale('symlog')
    # ax1.set_yscale('logit')
    plt.grid()
    return

main()

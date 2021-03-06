import matplotlib.lines as mlines
import matplotlib.patches as mpatches
import matplotlib.pyplot as plt
from numpy import genfromtxt
from random import betavariate


# global variables:
PLOT_NUMBER = 1
ROWS = 5
COLS = 3

def main():
    global PLOT_NUMBER
    f, axs = plt.subplots(ROWS, COLS, figsize=(9,10))
    # plt.suptitle('Influence of unknown data to prediction', fontsize=12, y=1, fontweight='bold')
    plt.NullFormatter()

    for pp in [10, 20, 30, 40, 50]: 
        plot_hist(pp)
        plot_data_unknown(pp)
        plot_data_multifurc(pp)

    plt.tight_layout()
    plt.show()
    # ------------------------------------------------------------------------
    # ------------------------------------------------------------------------

    f, axs = plt.subplots(1, 1, figsize=(4,3))

    # -------------------------------------plot distribution------------------------------------
    beta_distribution_parameters = [7, 5.5, 2.75, 7]   # 40 P - 60 FL
    #   for freeliving_distribution
    A_FL = beta_distribution_parameters[0]
    B_FL = beta_distribution_parameters[1]
    #   for parasite_distribution
    A_P = beta_distribution_parameters[2]
    B_P = beta_distribution_parameters[3]

    freeliving_distribution = []
    parasite_distribution = []
    for item in range(0, 1000000):
        freeliving_distribution.append(betavariate(A_FL, B_FL))
        parasite_distribution.append(betavariate(A_P, B_P))

    ax = plt.subplot(1, 1, 1)

    # the histogram of the data
    n, bins, patches = plt.hist(parasite_distribution, 100, normed=1, facecolor='r', alpha=0.75)
    n, bins, patches = plt.hist(freeliving_distribution, 100, normed=1, facecolor='b', alpha=0.75)

    plt.xlabel('drawn random number', fontsize=9)
    plt.ylabel('number of draws', fontsize=9)

    title = str(40) + '% P - ' + str(100-40) + '% FL'
    plt.axvline(x=40/100, color='black')#, xmin=0.25, xmax=0.402, linewidth=2)
    
    blue_patch = mpatches.Patch(color='blue', label='free-livings')
    red_patch = mpatches.Patch(color='red', label='parasites')
    black_line = mlines.Line2D([], [], color='black', label='threshold')#, marker='*', markersize=15)
    plt.legend(handles=[blue_patch, red_patch, black_line], title=title, loc="upper right", fontsize=9) # shadow=True, fancybox=True)
    ax.get_legend().get_title().set_fontweight("bold")
    # plt.axis([0, 1, 0, 8])
    plt.axis([0, 1, -0.2, 8])
    plt.grid(True)

    # -------------------------------------plot points------------------------------------
    plt.plot([0.15,0.33,0.52], [0,0,0], color='black', marker='o', markersize=10, markerfacecolor='red') #maroon
    plt.plot([0.44], [0], color='black', marker='o', markersize=10, markerfacecolor='blue') #navy
    ax.annotate('1', xy=(0.33, 0), xytext=(0.34, 0.1), color='white', fontweight='bold')
    ax.annotate('2', xy=(0.15, 0), xytext=(0.16, 0.1), color='white', fontweight='bold')
    ax.annotate('3', xy=(0.52, 0), xytext=(0.53, 0.1), color='white', fontweight='bold')
    ax.annotate('4', xy=(0.44, 0), xytext=(0.45, 0.1), color='white', fontweight='bold')
    plt.tight_layout()
    plt.show()
    # ------------------------------------------------------------------------
    # ------------------------------------------------------------------------

    PLOT_NUMBER = 1
    f, axs = plt.subplots(2, 2, figsize=(12, 5))
    # plt.suptitle('Fitch Versions and Unknown Data', fontsize=12, y=1)
    # filepath = 'data/simulation/30-fitch-unknown_plot.csv'
    filepath = 'data/simulation/fitch_30-unknown.csv'
    plt.subplot(2, 2, 1)
    plot_fitch_versions(filepath, 30)
    # filepath = 'data/simulation/40-fitch-unknown_plot.csv'
    filepath = 'data/simulation/fitch_40-unknown.csv'
    plt.subplot(2, 2, 2)
    plot_fitch_versions(filepath, 40)
    # filepath = 'data/simulation/50-fitch-unknown_plot.csv'
    filepath = 'data/simulation/fitch_50-unknown.csv'
    plt.subplot(2, 2, 3)
    plot_fitch_versions(filepath, 50)

    # plt.tight_layout()
    plt.show()

    return

def plot_hist(percentage_parasites):
    global PLOT_NUMBER
                                # [A_FL, B_FL, A_P, B_P]
    beta_distribution_parameters = [7, 3.5, 3.5, 7]   # 40 P - 60 FL

    # decide for distribution:
    if percentage_parasites == 10:
        beta_distribution_parameters = [7, 24, 0.5, 7]     # 10 P - 90 FL
    elif percentage_parasites == 20:
        beta_distribution_parameters = [7, 13.25, 1.25, 7] # 20 P - 80 FL
    elif percentage_parasites == 30:
        beta_distribution_parameters = [7, 8.5, 2, 7]      # 30 P - 70 FL
    elif percentage_parasites == 40:
        beta_distribution_parameters = [7, 5.5, 2.75, 7]   # 40 P - 60 FL
    elif percentage_parasites == 50:
        beta_distribution_parameters = [7, 3.5, 3.5, 7]    # 50 P - 50 FL


    # -------------------------------------plot distribution------------------------------------
    #   for freeliving_distribution
    A_FL = beta_distribution_parameters[0]
    B_FL = beta_distribution_parameters[1]
    #   for parasite_distribution
    A_P = beta_distribution_parameters[2]
    B_P = beta_distribution_parameters[3]

    freeliving_distribution = []
    parasite_distribution = []
    for item in range(0, 100000):
        freeliving_distribution.append(betavariate(A_FL, B_FL))
        parasite_distribution.append(betavariate(A_P, B_P))

    ax = plt.subplot(ROWS, COLS, PLOT_NUMBER)
    PLOT_NUMBER += 1

    # the histogram of the data
    n, bins, patches = plt.hist(parasite_distribution, 100, normed=1, facecolor='r', alpha=0.75)
    n, bins, patches = plt.hist(freeliving_distribution, 100, normed=1, facecolor='b', alpha=0.75)


    plt.ylabel('number of draws', fontsize=9)

    if PLOT_NUMBER == 1:
        plt.title('Histogram of distributions', fontweight='bold')
    if percentage_parasites != '40-old':
        title = str(percentage_parasites) + '% P - ' + str(100-percentage_parasites) + '% FL'
        plt.axvline(x=percentage_parasites/100, color='black')#, xmin=0.25, xmax=0.402, linewidth=2)
    else:
        title = '40 % P - 60 % FL'
        plt.axvline(x=.4, color='black')#, xmin=0.25, xmax=0.402, linewidth=2)
    blue_patch = mpatches.Patch(color='blue', label='free-livings')
    red_patch = mpatches.Patch(color='red', label='parasites')
    black_line = mlines.Line2D([], [], color='black', label='threshold')#, marker='*', markersize=15)
    plt.legend(handles=[blue_patch, red_patch, black_line], title=title, loc="upper right", fontsize=9) # shadow=True, fancybox=True)
    ax.get_legend().get_title().set_fontweight("bold")
    plt.axis([0, 1, 0, 8])
    if (PLOT_NUMBER == 14) or (PLOT_NUMBER == 8):
        plt.xlabel('drawn random number', fontsize=9)
    plt.grid(True)

    return

def plot_data_unknown(percentage_parasites):
    global PLOT_NUMBER
    filepath = 'data/simulation/' + str(percentage_parasites) + '-unknown.csv'
    data = genfromtxt(filepath, delimiter=',', skip_header=1, skip_footer=0, names=['unknown', 'multifurcation', 'y_fitch', 'y_my', 'y_sankoff'])

    plt.subplot(ROWS, COLS, PLOT_NUMBER)
    PLOT_NUMBER += 1

    # plt.title(str(percentage_parasites), fontweight='bold')
    plt.ylabel('correct predicted', fontsize=9)
    plt.plot(data['unknown'], data['y_fitch'], color='g', linestyle='dashed', 
        label='Fitch', linewidth=0.5, marker='.', markerfacecolor='black')#, markersize=5)
    # plt.plot(data['unknown'], data['y_my'], color='c', linestyle='dashed', 
    #     label='My', linewidth=0.5, marker='.', markerfacecolor='black')
    plt.plot(data['unknown'], data['y_sankoff'], color='m', linestyle='dashed', 
        label='Sankoff', linewidth=0.5, marker='.', markerfacecolor='black')
    plt.legend(loc="lower left", fontsize=9) #, scatterpoints=1, numpoints=2)
    plt.axis([0, 1, 50, 100])
    if (PLOT_NUMBER == 15) or (PLOT_NUMBER == 9):
        plt.xlabel('percentage unknown', fontsize=9)
    # else:
    #     plt.xticks([])
    plt.grid()
    return

def plot_data_multifurc(percentage_parasites):
    global PLOT_NUMBER
    filepath = 'data/simulation/' + str(percentage_parasites) + '-multifurcation.csv'
    data = genfromtxt(filepath, delimiter=',', skip_header=1, skip_footer=0, names=['unknown', 'multifurcation', 'y_fitch', 'y_my', 'y_sankoff'])

    plt.subplot(ROWS, COLS, PLOT_NUMBER)
    PLOT_NUMBER += 1

    # plt.title(str(percentage_parasites), fontweight='bold')
    plt.ylabel('correct predicted', fontsize=9)
    plt.plot(data['multifurcation'], data['y_fitch'], color='g', linestyle='dashed', 
        label='Fitch', linewidth=0.5, marker='.', markerfacecolor='black')#, markersize=5)
    # plt.plot(data['unknown'], data['y_my'], color='c', linestyle='dashed', 
    #     label='My', linewidth=0.5, marker='.', markerfacecolor='black')
    plt.plot(data['multifurcation'], data['y_sankoff'], color='m', linestyle='dashed', 
        label='Sankoff', linewidth=0.5, marker='.', markerfacecolor='black')
    if PLOT_NUMBER < 10:
        plt.legend(loc="lower left", fontsize=9) #, scatterpoints=1, numpoints=2)
    else: 
        plt.legend(loc="upper left", fontsize=9) #, scatterpoints=1, numpoints=2)
    plt.axis([0, 1, 50, 100])
    if (PLOT_NUMBER == 16) or (PLOT_NUMBER == 10):
        plt.xlabel('percentage multifurcation', fontsize=9)
    # else:
    #     plt.xticks([])
    plt.grid()
    return

def plot_fitch_versions(filepath, percentage_parasites):
    data = genfromtxt(filepath, delimiter=',', skip_header=1, skip_footer=0, names=['unknown', 'multifurcation','y_fitch1', 'y_fitch2', 'y_fitch3', 'y_fitch4'])

    # plt.title(str(percentage_parasites), fontweight='bold')
    plt.plot(data['unknown'], data['y_fitch1'], color='g', linestyle='dashed', 
        label='Fitch 1', linewidth=0.5, marker='.', markerfacecolor='black')#, markersize=5)
    plt.plot(data['unknown'], data['y_fitch2'], color='c', linestyle='dashed', 
        label='Fitch 2', linewidth=0.5, marker='.', markerfacecolor='black')
    plt.plot(data['unknown'], data['y_fitch3'], color='m', linestyle='dashed', 
        label='Fitch 3', linewidth=0.5, marker='.', markerfacecolor='black')
    plt.plot(data['unknown'], data['y_fitch4'], color='y', linestyle='dashed', 
        label='Fitch 4', linewidth=0.5, marker='.', markerfacecolor='black')
    plt.xlabel('percentage unknown', fontsize=9)
    plt.ylabel('correct predicted', fontsize=9)
    title = str(percentage_parasites) + '% P - ' + str(100-percentage_parasites) + '% FL'
    plt.legend(title=title, loc="lower left", fontsize=9) #, scatterpoints=1, numpoints=2)
    plt.axis([0, 1, 85, 100])
    plt.grid()

    return

main()

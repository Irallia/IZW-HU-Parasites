import matplotlib.pyplot as plt
import pandas as pd

path = '../data/labelled_supertree/ottnames-childrenPlot.csv'
# path = '../data/labelled_supertree/ottnames-childrenPlot-cellular_organisms.csv'
# path = '../data/labelled_supertree/ottnames-childrenPlot-eukaryota.csv'


data = pd.read_csv(path, header=None)
# print(data)

print(len(data))
# plt.hist(data, bins=154)
# plt.hist(data, bins=221)
# plt.hist(data, bins=154)
# plt.hist(data, bins=92)
plt.hist(data, bins=235)
# plt.xlim(0,31000)
# plt.xlim(0,8900)
# plt.xlim(0,31000)
# plt.xlim(0,1000)
# plt.xlim(0,5000)
# plt.xscale('log')
plt.yscale('log')
# plt.title("Children per Node - Cellular Organisms")
# plt.title("Children per Node - Eukaryota")
# plt.title("Children per Node - Bacteria")
# plt.title("Children per Node - Archaea")
plt.title("Children per Node - Metazoa")

plt.xlabel("#Children")
plt.ylabel("#Nodes*#Children")
# i = 30818/154
# i = 8855/221
# i = 30818/154
# i = 918/92
i = 4747/235
print(i)

# plt.text(22500, 100000, "width of bins = 200")
# plt.text(22500, 50000, "highest degree of node is 30818")
# plt.text(22500, 25000, "#nodes = 265641")
# plt.text(6500, 100000, "width of bins = 40")
# plt.text(6500, 50000, "highest degree of node is 8855")
# plt.text(6500, 25000, "#nodes = 243237")
# plt.text(20000, 10000, "width of bins = 200")
# plt.text(20000, 5000, "highest degree of node is 30818")
# plt.text(700, 400, "width of bins = 10")
# plt.text(700, 250, "highest degree of node is 919")
# plt.text(700, 150, "#nodes = 522")
plt.text(3500, 100000, "width of bins = 20")
plt.text(3500, 50000, "highest degree of node is 4747")
plt.text(3500, 25000, "#nodes = 180687")
plt.show()

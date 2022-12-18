import numpy as np
import matplotlib.pyplot as plt

file = np.loadtxt("manhattan.plot")
# remove SNPs with no location
file = file[file[:, 0] > 0]

# transpose
file = file.T

plt.scatter(file[0], file[1], s=4)
plt.xlabel('position of SNP')
plt.ylabel('-log10 of p value')
plt.savefig("manhattan_plot.png")
# plt.show()

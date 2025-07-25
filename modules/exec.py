import argparse
import os
import main
import matplotlib.pyplot as plt


plt.interactive(False)

parser = argparse.ArgumentParser()
parser.add_argument('csv', help='csv-file name')
parser.add_argument('--result', help='directory to export result-plot')

args = parser.parse_args()

analyzer = main.Analyzer(args.csv, args.result)
figure = analyzer._AUs_plot(1)
plt.show()
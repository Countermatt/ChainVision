#!/usr/bin/python

import csv
import matplotlib.pyplot as plt
import os
from math import floor

def main():
    dir_path = os.path.dirname(os.path.realpath(__file__))
    data_file = dir_path + "/figure_data/data.csv"
    plot_file = dir_path + "/plot/nb_empty_block.pdf"
    
    with open(data_file, 'r') as csvfile:
        data = []
        x_graduation = []
        nb_empty = []
        csvreader = csv.reader(csvfile)
        next(csvreader)
        #Collecting all data
        for row in csvreader:
            data.append(row)


        for x in data:
            x_graduation.append(int(x[0]))
            nb_empty.append(floor(float(x[1])))
        fig = plt.figure()
        fig.set_figwidth(6)
        fig.set_figheight(2)
        ax  = fig.add_subplot(1,1,1)
        ax.plot(x_graduation, nb_empty, color="grey", linestyle="-", label = "\% of Empty block")
        ax.set_xlabel("time in block windows")
        ax.set_ylabel("% empty block")
        ax.grid()
        plt.savefig(plot_file,  bbox_inches='tight', format = "pdf")

if __name__ == "__main__":
   main()
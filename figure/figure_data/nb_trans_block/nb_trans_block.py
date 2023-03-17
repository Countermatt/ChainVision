#!/usr/bin/python

import csv
import matplotlib.pyplot as plt
import os
from math import floor

def main():
    dir_path = os.path.dirname(os.path.realpath(__file__))
    data_file = dir_path + "/nb_trans_block.csv"
    plot_file = dir_path + "/plot/nb_trans_block.pdf"
    
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
            nb_empty.append(int(x[1]))
        fig = plt.figure()
        fig.set_figwidth(6)
        fig.set_figheight(2)
        ax  = fig.add_subplot(1,1,1)
        ax.plot(x_graduation, nb_empty, color="grey", linestyle="-", label = "number of transaction")
        ax.set_xlabel("time in block windows")
        ax.set_ylabel("number of transaction")
        ax.grid()
        plt.savefig(plot_file,  bbox_inches='tight', format = "pdf")
if __name__ == "__main__":
   main()
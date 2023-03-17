#!/usr/bin/python

##Import 
import csv
import matplotlib.pyplot as plt
import os
from math import inf
### This function return the list of gas use per block for a specified window ###

def sort_directory(list_file):
    result = []
    for x in list_file:
        if len(result) == 0:
            result.append(x)
        i = 1
        while i <= len(result):
            if i == 1:
                if int(result[-i].split("-")[0]) < int(x.split("-")[0]):
                   result.append(x)   
                   break
                
            elif i == len(result):
                if int(result[-i].split("-")[0]) > int(x.split("-")[0]):   
                    tmp = result
                    result = [x] + tmp
                    break
                else:
                    tmp1 = result[1:]
                    tmp2 = result[0]
                    result = [tmp2] + [x] + tmp1
                    break
            elif int(result[-i].split("-")[0]) < int(x.split("-")[0]) and int(result[-i+1].split("-")[0]) > int(x.split("-")[0]):
                tmp1 = result[0:-i+1]
                tmp2 = result[-i+1:len(result)]
                result = tmp1 + [x] + tmp2
                break
            i += 1
    return result

def main():

    dir_path = os.path.dirname(os.path.realpath(__file__))
    data_path = dir_path + "/../../data/raw_data/block"
    save_file = dir_path + "/../../figure/figure_data/nb_empty_block.csv"

    dir_list = os.listdir(data_path)
    dir_list = sort_directory(dir_list)
    tmp = int(dir_list[0].split("-")[0])
    last_block = 0
    first_block = inf
    nb_empty = []
    x_graduation = []
    i = 1
    k =True
    for file in dir_list:
        data = []
        print(i,"/",len(dir_list))
        empty = 0
        file = data_path + "/" + file
        if file.split(".")[-1] == "csv":
            with open(file, 'r') as csvfile:
                
            # creating a csv reader object
                csvreader = csv.reader(csvfile)
                next(csvreader)
            #Collecting all data
                for row in csvreader:
                    data.append(row)
            if k:
                first_block =int(data[0][0])
                k = False
            for x in data:
                if int(x[2]) == 0:
                    empty += 1
            if empty != 0:
                nb_empty.append(empty/len(data)*100)
            else:
                nb_empty.append(0)
            x_graduation.append(int(file.split("-")[-1].split(".")[0]))
            i += 1

    with open(save_file, 'w') as output_file:
        fieldnames = ['x_graduation', 'nb_empty']
        dict_writer = csv.DictWriter(output_file, fieldnames=fieldnames)
        dict_writer.writeheader()
        for i in range(len(nb_empty)):
            record = {}
            record['x_graduation'] = x_graduation[i]
            record['nb_empty'] = nb_empty[i]
            dict_writer.writerow(record)
            


if __name__ == "__main__":
   main()
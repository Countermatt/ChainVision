#!/usr/bin/python

import csv
import os
import multiprocessing
from threading import Thread
import threading
import time

def qsort(sets,left,right):

    #print("thead {0} is sorting {1}".format(threading.current_thread(), sets[left:right]))

    i = left
    j = right
    pivot = sets[int((left + right)/2)]
    temp = 0
    while(i <= j):
         while(pivot > sets[i]):
             i = i+1
         while(pivot < sets[j]):
             j = j-1
         if(i <= j):
             temp = sets[i]     
             sets[i] = sets[j]
             sets[j] = temp
             i = i + 1
             j = j - 1

    lthread = None
    rthread = None

    if (left < j):
        lthread = Thread(target = lambda: qsort(sets,left,j))
        lthread.start()

    if (i < right):
        rthread = Thread(target=lambda: qsort(sets,i,right))
        rthread.start()

    if lthread is not None: lthread.join()
    if rthread is not None: rthread.join()
    return sets


#Sort entry directory
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


#Read CSV
def read_csv(file):
    data = []
    with open(file, 'r') as csvfile:
        csvreader = csv.reader(csvfile)
        next(csvreader)
        for row in csvreader:
            data.append(row)
    return data

def get_data(data):
    result = []
    for x in data:
        if not x[2] in result:
            result.append(x[2])
        if not x[3] in result:
            result.append(x[3])
    return result

def remove_duplicate(data, index):

    result = []
    for i in range(index):
        for y in data[index]:
            if not y in data[i]:
                result.append(y)
        data[index] = result
        print(i)
    return result

if __name__ == '__main__':
    
    nb_cores = multiprocessing.cpu_count()
    nb_cores = 4

    dir_path = os.path.dirname(os.path.realpath(__file__))
    transaction_path = dir_path + "/../../data/raw_data/transaction"
    save_file = dir_path + "/../../data/processed_data/account/account_list.csv"

    dir_list = os.listdir(transaction_path)
    dir_list = sort_directory(dir_list)


    multiprocessing.freeze_support() # for Windows, also requires to be in the statement: if __name__ == '__main__'
    index = 0
    print(dir)
    for file in dir_list:

        print(file, " Progress")
        print("===Create account list:", index+1, "/", len(dir_list),"===")
        
        file = transaction_path + "/" + file
        data = read_csv(file)
        data_list = [[] for _ in range(nb_cores)]
        k = 0
        for x in data:
            if k == nb_cores:
                k = 0
            data_list[k].append(x)
            k += 1
        print(len(data_list[0]))
        #with multiprocessing.Pool(processes=nb_cores) as pool: # auto closing workers
        with multiprocessing.Pool(processes=4) as pool:
            results = pool.starmap(get_data, zip(data_list))
        result = list(results)
        print("===Remove Duplicate:", index+1, "/", len(dir_list),"===")
        accounts = []
        for x in list(result):
            accounts += x

        accounts = qsort(accounts,0,len(accounts) - 1)
        csv_list = []
        for x in range(1, len(accounts)):
            if accounts[x-1] != accounts[x]:
                csv_list.append(accounts[x])

        print("===wrtie csv:", index+1, "/", len(dir_list),"===")
        with open(save_file, 'a') as output_file:
            fieldnames = ['account']
            dict_writer = csv.DictWriter(output_file, fieldnames=fieldnames)
            dict_writer.writeheader()
            for account in csv_list:
                record = {}
                record['account'] = account
                dict_writer.writerow(record)
        print(file, " Done")
        index +=1

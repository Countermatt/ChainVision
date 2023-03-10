#!/usr/bin/python

import csv
import os
import multiprocessing


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
    result = set(())
    for x in data:
        result.add(x[2])
        result.add(x[3])
    return result

if __name__ == '__main__':
    
    nb_cores = multiprocessing.cpu_count()

    dir_path = os.path.dirname(os.path.realpath(__file__))
    transaction_path = dir_path + "/../../data/raw_data/transaction"
    save_directory = dir_path + "/../../data/processed_data/account/"

    dir_list = os.listdir(transaction_path)
    dir_list = sort_directory(dir_list) 

    multiprocessing.freeze_support() # for Windows, also requires to be in the statement: if __name__ == '__main__'
    index = 0
    for file in dir_list:
        print(file, " Progress")
        print("===Create account list:", index+1, "/", len(dir_list),"===")
        file_tmp = file
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
        with multiprocessing.Pool(processes=nb_cores) as pool: # auto closing workers
            results = pool.starmap(get_data, zip(data_list))
        account_set = set(())
        for x in results:
            account_set.update(x)

        print("===wrtie csv:", index+1, "/", len(dir_list),"===")
        with open(save_directory + file_tmp, 'a') as output_file:
            fieldnames = ['account']
            dict_writer = csv.DictWriter(output_file, fieldnames=fieldnames)
            dict_writer.writeheader()
            for account in account_set:
                record = {}
                record['account'] = account
                dict_writer.writerow(record)
        print(file, " Done")
        index +=1

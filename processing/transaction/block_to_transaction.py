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

def set_transaction(transaction, transaction_id):
    row = [transaction_id] + transaction[2:]
    return row

if __name__ == '__main__':
    
    dir_path = os.path.dirname(os.path.realpath(__file__))
    transaction_path = dir_path + "/../../data/raw_data/transaction"
    save_directory = dir_path + "/../../data/raw_data/transaction_order/"
    dir_list = os.listdir(transaction_path)
    dir_list = sort_directory(dir_list)


    multiprocessing.freeze_support() # for Windows, also requires to be in the statement: if __name__ == '__main__'
    index = 0
    dir_index = 0
    pending_data = []
    save_index = 0
    transaction_id = 0
    transaction_list = []
    while(dir_index < len(dir_list) or index < len(pending_data)):
        if(len(pending_data) < 10000 and dir_index < len(dir_list)):
            print("=== File Number:", dir_index+1, "/", len(dir_list),"===")
            pending_data = pending_data[index:] + read_csv(transaction_path + "/" + dir_list[dir_index])
            index = 0
            dir_index += 1
        if(len(transaction_list) == 10000):
            with open(save_directory + str(save_index) + ".csv", 'a') as output_file:
                fieldnames = ["transaction_index", "From","To","Value","Gas","Gas_price"]
                dict_writer = csv.DictWriter(output_file, fieldnames=fieldnames)
                dict_writer.writeheader()
                for account in transaction_list:
                    record = {}
                    record['transaction_index'] = account[0]
                    record['From'] = account[1]
                    record['To'] = account[2]
                    record['Value'] = account[3]
                    record['Gas'] = account[4]
                    record['Gas_price'] = account[5]
                    dict_writer.writerow(record)
            transaction_list = []
        transaction_list.append(set_transaction(pending_data[index], transaction_id))
        transaction_id +=1
        index +=1

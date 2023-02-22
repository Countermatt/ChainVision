import csv
import os
import multiprocessing

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

def account_trans(account, transaction_directory):
    with multiprocessing.Pool(processes=2) as pool:
        results = pool.map(get_trans, zip(account, dir_list))
    result = list(results)
    for x 

def get_trans(account, file):
    result = [[], []]
    data = []
    file = transaction_path + "/" + file[0]
    with open(file, 'r') as csvfile:
        csvreader = csv.reader(csvfile)
        next(csvreader)
        for row in csvreader:
            data.append(row)

    for x in data:
        if  str(x[2]) == str(account):
            result[0].append(x[2])
        if  str(x[3]) == str(account):
            result[1].append(x[3])
    return result

if __name__ == '__main__':
    
    dir_path = os.path.dirname(os.path.realpath(__file__))
    transaction_path = dir_path + "/../../data/raw_data/transaction"
    save_file = dir_path + "/../../data/processed_data/account/account_transactions.csv"
    account_file = dir_path + "/../../data/processed_data/account/account_list.csv"
    dir_list = os.listdir(transaction_path)
    dir_list = sort_directory(dir_list)

    accounts_list = read_csv(account_file)
    multiprocessing.freeze_support() # for Windows, also requires to be in the statement: if __name__ == '__main__'

    input_data = dir_list
    print("===Create account sub list===")
    #with multiprocessing.Pool(processes=nb_cores) as pool: # auto closing workers
    with multiprocessing.Pool(processes=2) as pool:
        results = pool.map(get_account_trans, zip(account_file))
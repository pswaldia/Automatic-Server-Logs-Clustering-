import pandas as pd
import numpy as np
import re
import os
import pickle
import sys


from collections import Counter
from collections import defaultdict


try:
    import ConfigParser
except ImportError:
    import configparser as ConfigParser


def get_options():
    cf = ConfigParser.ConfigParser()

    if os.path.exists("config.cof"):
        cf.read('config.cof')
    else:
        print("there is no config.cof!")
        exit()

    option_dict = dict()
    for key, value in cf.items("CLUSTER"):
        option_dict[key] = eval(value)

    return option_dict

option_dict = get_options()
filename = option_dict['filename']
clusters = option_dict['clusters']
maxx = option_dict['max']
minn = option_dict['min']
chars = option_dict['chars']    

def save_object(name, object):
    with open("{}_{}_cache/{}.pkl".format(filename, clusters, name), "wb") as f:
        pickle.dump(object, f)


def read_object(filename):
    with open(filename, "rb") as f:
        object = pickle.load(f)
    return object


def save_txt(name, object):
    with open("{}_{}_cache/{}.txt".format(filename, clusters, name), "w") as f:
        for item in object:
            f.write(str(item))
            f.write("\n")

def clear_log(line, chars):

    pattern_one = re.compile("[0-9]+")
    pattern_two = re.compile("|".join(chars))

    tmp_line = re.sub(pattern_one, "0", line)
    clearned_line = re.sub(pattern_two, "_", tmp_line).strip(" ").strip("_")

    return clearned_line


def load_log(filename,chars):

    documents = []
    count = 0
    import pandas
    data = [line.strip() for line in open(filename, "r").readlines()]
    data = [{"LineNumber": line.split('~')[0], "Text": line.split('~')[1]} for line in data]
    data = pandas.DataFrame(data)
    for i in range(data.shape[0]):
        line=data['Text'][i]
        cleared_line = clear_log(line, chars)
        documents.append(cleared_line)

    print(len(documents))

    return documents

def create_sub_files(database):
    if not os.path.exists("{}_{}_cache/cluster_files".format(filename, clusters)):
        os.mkdir("{}_{}_cache/cluster_files".format(filename, clusters))

    for key, value in database.items():
        with open("{}_{}_cache/cluster_files/cluster_{}.log".format(filename, clusters, key), "w") as f:
            for log in value:
                f.write(log)


def create_log_tag(labels, filename):
    label_dict = Counter(labels)
    labels_info = sorted(label_dict.items(), key=lambda item: item[1])
    database = defaultdict(list)
    index = 0

    with open(filename, mode="r", errors="replace") as f:
        while True:
            line = f.readline()
            if not line:
                break
            database[labels[index]].append(line)
            index += 1

    #save_object("database", database)
    create_sub_files(database)

    return database, labels_info




def create_view(labels_info, database):
    num = 5
    with open("{}_{}_cache/result.txt".format(filename, clusters), "w") as f:
        f.write("log information: \n\n")
        for item in labels_info:
            f.write("category {}, number: {}\n".format(item[0], item[1]))
        f.write("\n----------------------------------------\n")
        f.write("\nthe example logs are: \n")

        for category in labels_info:
            f.write("\ncategory {}\n".format(category[0]))
            if num <= len(database[category[0]]):
                for log in database[category[0]][0:num]:
                    f.write(log)
            else:
                for log in database[category[0]]:
                    f.write(log)
                    
def create_view_test(labels_info, database):
    num = 5
    with open("{}_{}_cache/result_test.txt".format(filename, clusters), "w") as f:
        f.write("log information: \n\n")
        for item in labels_info:
            f.write("category {}, number: {}\n".format(item[0], item[1]))
        f.write("\n----------------------------------------\n")
        f.write("\nthe example logs are: \n")

        for category in labels_info:
            f.write("\ncategory {}\n".format(category[0]))
            if num <= len(database[category[0]]):
                for log in database[category[0]][0:num]:
                    f.write(log)
            else:
                for log in database[category[0]]:
                    f.write(log)
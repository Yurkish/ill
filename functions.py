import csv
import datetime
import time
import numpy as np
import matplotlib.pyplot as plt
from scipy.interpolate import interp1d
from tkinter import *
from scipy import stats
from graphics import *

kind_lst = ['nearest', 'zero', 'slinear', 'cubic', 'previous', 'next']

def dividing_lists(w, ratio):
    if ratio > 1:
        ratio = 1
        print('ratio cannot be reater than 1')
    time_points_w_train = int(len(w)*ratio)
    w_train = w[:time_points_w_train]
    w_test = w[time_points_w_train:]
    return w_train, w_test

def import_csv_temperature(csvfilename,delim):
    data = []
    with open(csvfilename, "r", encoding="utf-8", errors="ignore") as scraped:
        reader = csv.DictReader(scraped, delimiter=delim)
        # header = reader.fieldnames
        row_index = 0
        for rowincsv in reader:
            if rowincsv:  # avoid blank lines
                row_index += 1
                columns = [str(row_index), str_to_ts_converter(rowincsv['ts_temperature']) , float(rowincsv['temperature'])]
                data.append(columns)
        print(csvfilename, ' - begins at: ', datetime.datetime.fromtimestamp(float(data[1][1])))
        print(csvfilename, ' - ends at  : ', datetime.datetime.fromtimestamp(float(data[-1][1])))
        print(csvfilename, ' - begins at: ', data[1][1])
        print(csvfilename, ' - ends at  : ', data[-1][1])
    return data

def import_csv_illumination(csvfilename,delim):
    data = []
    with open(csvfilename, "r", encoding="utf-8", errors="ignore") as scraped:
        reader = csv.DictReader(scraped, delimiter=delim)
        # header = reader.fieldnames
        row_index = 0
        for rowincsv in reader:
            if rowincsv:  # avoid blank lines
                row_index += 1
                columns = [str(row_index), str_to_ts_converter(rowincsv['ts_illumination']) , float(rowincsv['illumination'])]
                data.append(columns)
        print(csvfilename, ' - begins at: ', datetime.datetime.fromtimestamp(float(data[1][1])))
        print(csvfilename, ' - ends at  : ', datetime.datetime.fromtimestamp(float(data[-1][1])))
        print(csvfilename, ' - begins at: ', data[1][1])
        print(csvfilename, ' - ends at  : ', data[-1][1])
    return data

def import_csv_meteostation_Temperature(csvfilename,delim):
    data = []
    with open(csvfilename, "r", encoding="utf-8", errors="ignore") as scraped:
        reader = csv.DictReader(scraped, delimiter=delim)
        # header = reader.fieldnames
        row_index = 0

        mean_temp = np.mean
        for rowincsv in reader:
            if rowincsv:  # avoid blank lines
                row_index += 1
                columns = [str(row_index), rowincsv['ts'], float(rowincsv['Temperature'])]
                data.append(columns)
        print(csvfilename, ' - begins at: ', datetime.datetime.fromtimestamp(float(data[1][1])))
        print(csvfilename, ' - ends at  : ', datetime.datetime.fromtimestamp(float(data[-1][1])))
        print(csvfilename, ' - begins at: ', data[1][1])
        print(csvfilename, ' - ends at  : ', data[-1][1])
        print(row_index)
    return data

def str_to_ts_converter(string):
    element = datetime.datetime.strptime(string,'%Y-%m-%d %H:%M:%S')
    ts = datetime.datetime.timestamp(element)
    return ts

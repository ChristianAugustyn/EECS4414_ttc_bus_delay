import numpy as np # linear algebra
import pandas as pd # data processing, CSV file I/O (e.g. pd.read_csv)
import matplotlib.pyplot as plt
import datetime as dt
# common imports
import zipfile
import time
# import datetime, timedelta
import datetime
from datetime import datetime, timedelta
from datetime import date
from dateutil import relativedelta
from io import StringIO
import pandas as pd
import pickle
# from sklearn.base import BaseEstimator
# from sklearn.base import TransformerMixin
from io import StringIO
import requests
import json
# from sklearn.preprocessing import LabelEncoder, MinMaxScaler, StandardScaler
# from sklearn.model_selection import train_test_split
import matplotlib.pyplot as plt
import os
import math
from subprocess import check_output
# import seaborn as sns
# from IPython.display import display
import logging

import re
import os

load_from_scratch = True
# control whether to save dataframe with transformed data
save_transformed_dataframe = True
# control whether rows containing erroneous values are removed from the saved dataset
remove_bad_values = True
# name of file containing pickled dataframe version of input (unprocessed) dataset
pickled_input_dataframe = '2018_2020_df.pkl'
# name of file to which prepared data set is saved as a pickled dataframe
pickled_output_dataframe = '2018_2020_df_cleaned_remove_bad.pkl'

valid_vehicles = list(range(1000,1150))+ list(range(2000,2111)) + list(range(2150,2156)) + list(range(2240,2486))
valid_vehicles = valid_vehicles + list(range(2600,2620)) + list(range(2700,2766)) + list(range(2767,2859))
valid_vehicles = valid_vehicles + list(range(7000,7135)) + list(range(7400,7450)) + list(range(7500,7620)) + list(range(7620,7882))
valid_vehicles = valid_vehicles + list(range(8000,8100)) + list(range(9000,9027))

valid_directions = ['e','w','n','s','b']

valid_days = ['Monday','Tuesday','Wednesday','Thursday','Friday','Saturday','Sunday']

def get_path():
    return os.path.abspath(os.path.join(os.getcwd(), "data")) + "\\"

#Gets the list of all ttc xlsx files in the path
def get_ttc_data_list(path):
    files = os.listdir(path)
    files_xls = [f for f in files if f[-4:] == 'xlsx']
    # print(files)
    # print(files_xls)
    return(files_xls)

#laods the tabs of all the xls files in the list of xls files
def load_ttc_data(path, files, firstfile, firstsheet, df):
    for f in files:
        print("file name",f)
        xlsf = pd.ExcelFile(path+f)
        # iterate through sheets
        for sheet_name in xlsf.sheet_names:
            print("sheet_name",sheet_name)
            if (f != firstfile) or (sheet_name != firstsheet):
                print("sheet_name in loop",sheet_name)
                data = pd.read_excel(path+f,sheet_name=sheet_name)    
                df = df.append(data)
    return(df)

#takes the path and the file name, loads the xls files into a dataframe and saves it
def reloader(path, picklename):
    files = get_ttc_data_list(path)
    # print("list of xls", files)
    dfnew = pd.read_excel(path + files[0])
    #gets the list of sheets in the excel file
    xlsf = pd.ExcelFile(path+files[0])
    #pass the first file and first sheet
    dflatest = load_ttc_data(path, files, files[0], xlsf.sheet_names[0], dfnew)
    #save the dataframe and pickle it
    dflatest.to_pickle(path + picklename)

    return(dflatest)

#create input categories for columns
def define_feature_categories(df):
    allcols = list(df)
    print("all cols",allcols)
    textcols = ['Incident','Location'] # 
    continuouscols = ['Min Delay','Min Gap'] 
                      # columns to deal with as continuous values - no embeddings
    timecols = ['Report Date','Time']
    collist = ['Day','Vehicle','Route','Direction']
    for col in continuouscols:
        df[col] = df[col].astype(float)
    print('texcols: ',textcols)
    print('continuouscols: ',continuouscols)
    print('timecols: ',timecols)
    print('collist: ',collist)
    return(allcols,textcols,continuouscols,timecols,collist)

# fill missing values according to the column category
def fill_missing(dataset,allcols,textcols,continuouscols,timecols,collist):
    logging.debug("before mv")
    for col in collist:
        dataset[col].fillna(value="missing", inplace=True)
    for col in continuouscols:
        dataset[col].fillna(value=0.0,inplace=True)
    for col in textcols:
        dataset[col].fillna(value="missing", inplace=True)
    return (dataset)

# read in data, either from original XLS files in data directory or from pickled dataframe containing
def ingest_data(path):
    if load_from_scratch:
        unpickled_df = reloader(path,pickled_input_dataframe)
        logging.debug("reloader done")
    else:
        unpickled_df = pd.read_pickle(path+pickled_input_dataframe)
    return(unpickled_df)

def fix_anomalous_columns(df):
    # for rows where there is NaN in the Min Delay or Min Gap columns, copy over value from Delay or Gap
    # df.Temp_Rating.fillna(df.Farheit, inplace=True)
    df['Min Delay'].fillna(df['Delay'], inplace=True)
    df['Min Gap'].fillna(df['Gap'], inplace=True)
    # now that the useful values have been copied from Delay and Gap, remove them
    del df['Delay']
    del df['Gap']
    # remove Incident ID column - it's extraneous
    del df['Incident ID']
    return(df)

def replace_time(date_time_value,time_value):
    ''' given a datetime replace the time portion '''
    print(date_time_value, time_value)
    if (isinstance(time_value, str)):
        try:
            time = datetime.strptime(time_value, "%H:%M:%S %p")
        except:
            #accouint for change in time format for august 2020 and onwards
            time = datetime.strptime(time_value, "%H:%M")
    else:
        time = time_value

    date_time_value = date_time_value.replace(hour=time.hour,minute=time.minute,second=time.second)
    return(date_time_value)

def general_cleanup(df):
    # ensure Route and Vehicle are strings, not numeric
    df['Route'] = df['Route'].astype(str)
    df['Vehicle'] = df['Vehicle'].astype(str)
    # remove extraneous characters left from Vehicle values being floats
    df['Vehicle'] = df['Vehicle'].str[:-2]
    # tactical definition of categories
    allcols,textcols,continuouscols,timecols,collist = define_feature_categories(df)
    # fill in missing values
    df.isnull().sum(axis = 0)
    df = fix_anomalous_columns(df)
    df = fill_missing(df,allcols,textcols,continuouscols,timecols,collist)
    # create new column combining date + time (needed for resampling) and make it the index
    df['Report Date Time'] = df.apply(lambda x: replace_time(x['Report Date'], x['Time']), axis=1)
    df.index = df['Report Date Time']
    # return the updated dataframe along with the column category lists
    return(df,allcols,textcols,continuouscols,timecols,collist)

### CLEAN UP ROUTINE ###

#NOT SURE
# def check_route (x):
#     if x in valid_routes:
#         return(x)
#     else:
#         return("bad route")

# def route_cleanup(df):
#     print("Route count pre cleanup",df['Route'].nunique())
#     # df['Route'].value_counts()
#     # replace bad route with common token
#     df['Route'] = df['Route'].apply(lambda x:check_route(x))
#     print("route count post cleanup",df['Route'].nunique())
#     return(df) 

def check_vehicle (x):
    if str.isdigit(x):
        if int(x) in valid_vehicles:
            return x
        else:
            return("bad vehicle")
    else:
        return("bad vehicle")

def vehicle_cleanup(df):
    print("Vehicle count pre cleanup",df['Vehicle'].nunique())
    df['Vehicle'] = df['Vehicle'].apply(lambda x:check_vehicle(x))
    print("Vehicle count post cleanup",df['Vehicle'].nunique())
    return(df)

def check_direction (x):
    if x in valid_directions:
        return(x)
    else:
        return("bad direction")

def direction_cleanup(df):
    print("Direction count pre cleanup",df['Direction'].nunique())
    df['Direction'] = df['Direction'].str.lower()
    df['Direction'] = df['Direction'].str.replace('/','')
    df['Direction'] = df['Direction'].replace({'eastbound':'e','westbound':'w','southbound':'s','northbound':'n'})
    df['Direction'] = df['Direction'].replace('b','',regex=True)
    df['Direction'] = df['Direction'].apply(lambda x:check_direction(x))
    print("Direction count post cleanup",df['Direction'].nunique())
    return(df)

def clean_conjunction(intersection):
    intersection = re.sub(" *& *"," and ",intersection)
    intersection = re.sub(" */ *"," and ",intersection)
    return(intersection)

def order_location(intersection):
    # for any string with the format "* and *" if the value before the and is alphabetically
    # higher than the value after the and, swap the values
    conj = " and "
    alpha_ordered_intersection = intersection
    if conj in intersection:
        end_first_street = intersection.find(conj)
        if (end_first_street > 0) and (len(intersection) > (end_first_street + len(conj))):
            start_second_street = intersection.find(conj) + len(conj)
            first_street = intersection[0:end_first_street]
            second_street = intersection[start_second_street:]
            alpha_ordered_intersection = min(first_street,second_street)+conj+max(first_street,second_street)
    return(alpha_ordered_intersection)

def location_cleanup(df):
    print("Location count pre cleanup",df['Location'].nunique())
    # make all location values lower case
    df['Location'] = df['Location'].str.lower()
    # make substitutions to eliminate obvious duplicate tokens
    df['Location'] = df['Location'].replace({'broadviewstation':'broadview station',' at ':' and ',' stn':' station',' ave.':'','/':' and ','roncy':'roncesvalles','carhouse':'yard','yard.':'yard','st. clair':'st clair','ronc. ':'roncesvalles ','long branch':'longbranch','garage':'yard','barns':'yard',' & ':' and '}, regex=True)
    # put intersection values into consistent order
    df['Location'] = df['Location'].apply(lambda x:order_location(x))
    print("Location count post cleanup",df['Location'].nunique())
    return(df)

#remove rows with bad values
def remove_bad(df):
    df = df[df.Vehicle != 'bad vehicle']
    df = df[df.Direction != 'bad direction']
    df = df[df.Route != 'bad route']
    return(df)

### MASTER ROUTINE###

path = get_path()
print("path is ",path)
# load route direction and delay data datframes
df = ingest_data(path)
print("number of records: ",len(df.index))
print("df.info() output",df.info())
print("df.shape output",df.shape)
print("df.describe() output",df.describe())
print("df.types output",df.dtypes)
df,allcols,textcols,continuouscols,timecols,collist = general_cleanup(df)
df.head()
# get record count by year
from collections import Counter
df_year = pd.DatetimeIndex(df['Report Date Time']).year
print("record count by year pre processing: ", str(Counter(df_year)))
# check that the values for April 2019 are correct
df[df['Report Date Time'].astype(str).str[:7]=='2019-04']
# cleanup Route
logging.debug("df.shape output pre route cleanup",df.shape)
#not sure if this is doable
# df = route_cleanup(df) 
df = vehicle_cleanup(df)
df = direction_cleanup(df)
df = location_cleanup(df)
logging.debug("df.shape output post location",df.shape)
if remove_bad_values:
    df = remove_bad(df)
print("Bad route count:",df[df.Route == 'bad route'].shape[0])
print("Bad direction count:",df[df.Direction == 'bad direction'].shape[0])
print("Bad vehicle count:",df[df.Vehicle == 'bad vehicle'].shape[0])
# pickle the cleansed dataframe
print("df.shape output post removal of bad records ",df.shape)
if save_transformed_dataframe:
    file_name = path + pickled_output_dataframe
    df.to_pickle(file_name)
df.head()
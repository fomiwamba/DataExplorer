import os
import pandas as pd
import datetime
import time

time.sleep (1)  # Warte 60 seconds

# Get File List + Channel List
print ("%" * 30)
print ("%" * 30)
# Load the assetfolder list
file = 'C:' + os.sep + 'BDA' + os.sep + 'ExpertAnalysis' + os.sep + 'PythonInput.txt'
# C:\BDA\TrendDataAnalysis\PythonInput.txt
f = open (file, 'r')
FileList = []
count = 0
for line in f:
    file_i = line[:-1]
    FileList.append (file_i)
f.close ()

print ("%" * 30)
print ("%" * 30)
print (FileList)
folder = os.path.split (FileList[0])[0]
folder_parts = folder.split (
    '\\')  # folder_parts = ['D:', 'Projekte', 'CNT_SUES', 'Output', 'Process', '2020', '01', '23']
print (folder_parts)

inputfolder = folder + os.sep
outputfolder = folder + os.sep

# -----------------------------------------------------------------------------------------------------------------------
# Collect All ChName_Parameter.csv vertically
files = FileList

if len (files) > 0:
    # 2) append all chname_parametertables to build a featuretable
    count = 0
    for file_i in files:
        print (count, '--->', file_i)
        if count == 0:
            df = pd.read_csv (file_i, sep=';', decimal=',', low_memory=False,
                              encoding='unicode_escape')  # , low_memory=False
            print ('df size: ', df.shape)
            # print (df.head (5))
        else:
            df_new = pd.read_csv (file_i, sep=';', decimal=',', low_memory=False)
            print ('df_new size: ', df_new.shape)
            # print (df.head (5))
            df = df.append (df_new, ignore_index=True)  # df = pd.concat ([df, df_new], axis=1, sort=False)
            print ('df size: ', df.shape)

        count = count + 1

    df = df.T.drop_duplicates ().T  # df = df.loc[:, ~df.columns.duplicated ()]
    df.fillna (0, inplace=True)

    # df = ChangeFormatDateTime (df)# nicht notwendig, diese Daten sind schon von python und nicht von imc famos
    correct_date_time = False
    if correct_date_time:
        date_vec = df.Date_Time
        datetime_obj_vec = []
        for ii in range (len (date_vec)):
            date_time_str = str (date_vec[ii])
            dd = date_time_str[0:2]
            mm = date_time_str[3:5]
            yy = date_time_str[6:8]
            hh = date_time_str[9:11]
            mn = date_time_str[12:14]
            ss = date_time_str[15:17]
            datetime_str = yy + '-' + mm + '-' + dd + ' ' + hh + ':' + mn + ':' + ss
            if len (datetime_str) != 17:
                print (ii, datetime_str)
            datetime_obj = datetime.datetime.strptime (datetime_str, "%y-%m-%d %H:%M:%S")
            datetime_obj1 = datetime_obj  # + ii*datetime.timedelta (seconds=delta_time)
            datetime_obj2 = datetime_obj1.strftime ("%Y-%m-%d %H:%M:%S")
            datetime_obj_vec.append (datetime_obj2)
        df.drop ('Date_Time', axis=1, inplace=True)
        df.insert (loc=0, column='Date_Time', value=datetime_obj_vec)
        df['Date_Time'] = df.Date_Time.astype ('datetime64[ns]')
        df.Date_Time = datetime_obj_vec
    else:
        df['Date_Time'] = pd.to_datetime (df['Date_Time'], format='%Y-%m-%d %H:%M:%S', errors='ignore')

    if 'Date_Time' in df.columns:
        df1 = df.pop ('Date_Time')  # remove column Date_Time and store it in df1
        df.insert (0, 'Date_Time', df1)  # add Date_Time as 1st column.
		
    df.sort_values (by='Date_Time', axis=0, inplace=True, ascending=True)  # Sortierung nach Date_Time
    df.index = range (len (df.index))
    print (df.Date_Time.head (5))

    if "Output" not in folder_parts:
        outputfolder_ = folder_parts[0] + os.sep + folder_parts[1] + os.sep + folder_parts[2] + os.sep + folder_parts[
            3] + os.sep  # + folder_parts[4]+os.sep
    else:
        outputfolder_ = folder_parts[0] + os.sep + folder_parts[1] + os.sep + folder_parts[2] + os.sep + folder_parts[
        3] + os.sep + folder_parts[4] + os.sep

    filename = outputfolder_ + 'AppendFileFromTo.csv';
    df.to_csv (filename, index=False, sep=';', decimal=',')
    print (filename, ' successfully created')

time.sleep (1)  # Warte 60 seconds

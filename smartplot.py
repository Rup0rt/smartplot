#!/usr/bin/env python3

import sys
import time
import datetime
import matplotlib.pyplot as plt
import matplotlib.dates as pltdates
from matplotlib.backends.backend_pdf import PdfPages

# config data
outputfile = "output.pdf"
lastdays = 0
event = ""

# init S.M.A.R.T. ids
idstr = { 1: "Raw_Read_Error_Rate",
          2: "Throughput_Performance",
          3: "Spin_Up_Time",
          4: "Start_Stop_Count",
          5: "Reallocated_Sector_Ct",
          7: "Seek_Error_Rate",
          8: "Seek_Time_Performance",
          9: "Power_On_Hours",
          10: "Spin_Retry_Count",
          11: "Calibration_Retry_Count",
          12: "Power_Cycle_Count",
          184: "End-to-End_Error",
          187: "Reported_Uncorrect",
          188: "Command_Timeout",
          190: "Airflow_Temperature_Cel",
          192: "Power-Off_Retract_Count",
          193: "Load_Cycle_Count",
          194: "Temperature_Celsius",
          195: "Hardware_ECC_Recovered",
          196: "Reallocated_Event_Count",
          197: "Current_Pending_Sector",
          198: "Offline_Uncorrectable",
          199: "UDMA_CRC_Error_Count",
          200: "Multi_Zone_Error_Rate",
          201: "Soft_Read_Error_Rate",
          221: "G-Sense_Error_Rate",
          225: "Load-Unload_Cycle_Count",
          228: "Power-Off_Retract_Cycle" }

# get filename
if len(sys.argv) != 2:
  print("Usage: " + sys.argv[0] + " <CSVFILE>")
  exit(1)

source = sys.argv[1]

# prepare plot arrays
times = []
data = {}

# calc last day timestamp
tslimit = time.time() - (lastdays*24*60*60)

# calc event ts
if event != "":
  eventts = time.mktime(datetime.datetime.strptime(event, "%d.%m.%Y %H:%M").timetuple())
  eventobj = datetime.datetime.fromtimestamp(eventts)

# since smartd uses 2-character-separator (;\t), we need to split ourself
csvfile = open(source, "r")
while True:
  line = csvfile.readline()
  if len(line) == 0: break

  # split line
  parts = line.split(";\t")
  timeval = parts[0]

  # skip entry if daylimit is not reached
  if (lastdays > 0):
    # calc ts (example: 2016-11-18 13:13:59)
    ts = time.mktime(datetime.datetime.strptime(timeval, "%Y-%m-%d %H:%M:%S").timetuple())
    # limit reached?
    if ts < tslimit:
      continue

  # collect time
  times.append(timeval)

  # handle attributes
  for part in parts[1:]:
    attrs = part.split(";")
    id = int(attrs[0])
    value = int(attrs[1])
    rawvalue = int(attrs[2])

    # prepare array
    if not id in data:
      data[id] = { 'raw': [], 'value': [] }

    # collect data in array
    data[id]['raw'].append(rawvalue)
    data[id]['value'].append(value)

csvfile.close()

# output stats
print("Time range: " + times[0] + " - " + times[-1])
print("Got " + str(len(times)) + " values...")

# prepare PDF
with PdfPages(outputfile) as pdf:
  # fill pdf info data
  info = pdf.infodict()
  info['Title'] = 'Analysis of ' + source
  info['Author'] = 'smartplot'
  info['Subject'] = 'Analysis of ' + source
  info['Keywords'] = 'S.M.A.R.T. hdd disk analysis'
  info['CreationDate'] = datetime.datetime(2009, 11, 13)
  info['ModDate'] = datetime.datetime.today()

  # plot data
  for id in data:
    # get proper id name string
    if id in idstr:
      idname = idstr[id]
    else:
      idname = "Unknown_HDD_Attribute_" + str(id)

    print("Plotting " + idname + "...")

    # plot raw value
    plt.figure(figsize=(20,10))
    plt.title(idname + " (RAW_VALUE)")
    dates = pltdates.datestr2num(times)
    plt.plot_date(dates, data[id]['raw'], 'black')
    plt.ylabel("Value")
    plt.xlabel("Time")
    if event != "":
      plt.axvline(x=eventobj, color='r', linestyle='--')
    pdf.savefig()
    plt.close()

    # plot value
    plt.figure(figsize=(20,10))
    plt.title(idname + " (VALUE)")
    dates = pltdates.datestr2num(times)
    plt.plot_date(dates, data[id]['value'], 'b')
    plt.ylabel("Value")
    plt.xlabel("Time")
    if event != "":
      plt.axvline(x=eventobj, color='r', linestyle='--')
    pdf.savefig()
    plt.close()

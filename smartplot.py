#!/usr/bin/env python3

import sys
import matplotlib.pyplot as plt
import matplotlib.dates as pltdates

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
          12: "Power_Cycle_Count",
          192: "Power-Off_Retract_Count",
          193: "Load_Cycle_Count",
          194: "Temperature_Celsius",
          196: "Reallocated_Event_Count",
          197: "Current_Pending_Sector",
          198: "Offline_Uncorrectable",
          199: "UDMA_CRC_Error_Count" }

# get filename
if len(sys.argv) != 2:
  print("Usage: " + sys.argv[0] + " <CSVFILE>")
  exit(1)

source = sys.argv[1]

# prepare plot arrays
times = []
data = {}

# since smartd uses 2-character-separator (;\t), we need to split ourself
csvfile = open(source, "r")
while True:
  line = csvfile.readline()
  if len(line) == 0: break

  # split line
  parts = line.split(";\t")
  timeval = parts[0]

  # collect time (example: 2016-11-18 13:13:59)
  times.append(timeval)

  # handle attributes
  for part in parts[1:]:
    attrs = part.split(";")
    id = int(attrs[0])
    value = int(attrs[1])
    rawvalue = int(attrs[2])

    # prepare array
    if not id in data:
      data[id] = []

    # collect data in array
    data[id].append(rawvalue)

csvfile.close()

# output stats
print("Time range: " + times[0] + " - " + times[-1])
print("Got " + str(len(times)) + " values...")

# plot data
for id in data:
  idname = idstr[id]
  print("Plotting " + idname + "...")

  plt.title(idname)
  dates = pltdates.datestr2num(times)
  plt.plot_date(dates, data[id])
  plt.ylabel("Raw Value")
  plt.xlabel("Time")
  plt.show()

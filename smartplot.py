#!/usr/bin/env python3

import sys
import matplotlib.pyplot as plt
import matplotlib.dates as pltdates

# get filename
if len(sys.argv) != 2:
  print("Usage: " + sys.argv[0] + " <CSVFILE>")
  exit(1)

source = sys.argv[1]

# into plot arrays
times = []
rawread = []
spinup = []
startstop = []
reallocsct = []
seekerror = []
poweron = []
spinretry = []
caliretry = []
powercycle = []
unknown180 = []
e2eerror = []
repuncorrect = []
comtimeout = []
airflowtemp = []
poffretract = []
loadcycle = []
temp = []
hweccrec = []
reallocev = []
pendingsct = []
offluncorr = []
crcerror = []
mzerror = []

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

    # collect Raw_Read_Error_Rate (id 1)
    if (id == 1):
      rawread.append(rawvalue)

    # collect Spin_Up_Time (id 3)
    if (id == 3):
      spinup.append(rawvalue)

    # collect Start_Stop_Count (id 4)
    if (id == 4):
      startstop.append(rawvalue)

    # collect Reallocated_Sector_Ct (id 5)
    if (id == 5):
      reallocsct.append(rawvalue)

    # collect Seek_Error_Rate (id 7)
    if (id == 7):
      seekerror.append(rawvalue)

    # collect Power_On_Hours (id 9)
    if (id == 9):
      poweron.append(rawvalue)

    # Spin_Retry_Count (id 10)
    if (id == 10):
      spinretry.append(rawvalue)

    # Calibration_Retry_Count (id 11)
    if (id == 11):
      caliretry.append(rawvalue)

    # Power_Cycle_Count (id 12)
    if (id == 12):
      powercycle.append(rawvalue)

    # Unknown_HDD_Attribute (id 180)
    if (id == 180):
      unknown180.append(rawvalue)

    # End-to-End_Error (id 184)
    if (id == 184):
      e2eerror.append(rawvalue)

    # Reported_Uncorrect (id 187)
    if (id == 187):
      repuncorrect.append(rawvalue)

    # Command_Timeout (id 188)
    if (id == 188):
      comtimeout.append(rawvalue)

    # Airflow_Temperature_Cel (id 190)
    if (id == 190):
      airflowtemp.append(rawvalue)

    # Power-Off_Retract_Count (id 192)
    if (id == 192):
      poffretract.append(rawvalue)

    # Load_Cycle_Count (id 193)
    if (id == 193):
      loadcycle.append(rawvalue)

    # Temperature_Celsius (id 194)
    if (id == 194):
      temp.append(rawvalue)

    # Hardware_ECC_Recovered (id 195)
    if (id == 195):
      hweccrec.append(rawvalue)

    # Reallocated_Event_Count (id 196)
    if (id == 196):
      reallocev.append(rawvalue)

    # Current_Pending_Sector (id 197)
    if (id == 197):
      pendingsct.append(rawvalue)

    # Offline_Uncorrectable (id 198)
    if (id == 198):
      offluncorr.append(rawvalue)

    # UDMA_CRC_Error_Count (id 199)
    if (id == 199):
      crcerror.append(rawvalue)

    # Multi_Zone_Error_Rate (id 200)
    if (id == 200):
      mzerror.append(rawvalue)

csvfile.close()

print("Time range: " + times[0] + " - " + times[-1])
print("Plotting " + str(len(times)) + " values...")


plt.title("Raw_Read_Error_Rate")
dates = pltdates.datestr2num(times)
plt.plot_date(dates, rawread)
plt.ylabel("Raw Value")
plt.xlabel("Time")
plt.show()

plt.title("Spin_Up_Time")
dates = pltdates.datestr2num(times)
plt.plot_date(dates, spinup)
plt.ylabel("Raw Value")
plt.xlabel("Time")
plt.show()

plt.title("Start_Stop_Count")
dates = pltdates.datestr2num(times)
plt.plot_date(dates, startstop)
plt.ylabel("Raw Value")
plt.xlabel("Time")
plt.show()

plt.title("Reallocated_Sector_Ct")
dates = pltdates.datestr2num(times)
plt.plot_date(dates, reallocsct)
plt.ylabel("Raw Value")
plt.xlabel("Time")
plt.show()

plt.title("Seek_Error_Rate")
dates = pltdates.datestr2num(times)
plt.plot_date(dates, seekerror)
plt.ylabel("Raw Value")
plt.xlabel("Time")
plt.show()

plt.title("Power_On_Hours")
dates = pltdates.datestr2num(times)
plt.plot_date(dates, poweron)
plt.ylabel("Raw Value")
plt.xlabel("Time")
plt.show()

plt.title("Spin_Retry_Count")
dates = pltdates.datestr2num(times)
plt.plot_date(dates, spinretry)
plt.ylabel("Raw Value")
plt.xlabel("Time")
plt.show()

plt.title("Calibration_Retry_Count")
dates = pltdates.datestr2num(times)
plt.plot_date(dates, caliretry)
plt.ylabel("Raw Value")
plt.xlabel("Time")
plt.show()

plt.title("Power_Cycle_Count")
dates = pltdates.datestr2num(times)
plt.plot_date(dates, powercycle)
plt.ylabel("Raw Value")
plt.xlabel("Time")
plt.show()

plt.title("Unknown_HDD_Attribute (180)")
dates = pltdates.datestr2num(times)
plt.plot_date(dates, unknown180)
plt.ylabel("Raw Value")
plt.xlabel("Time")
plt.show()

plt.title("End-to-End_Error")
dates = pltdates.datestr2num(times)
plt.plot_date(dates, e2eerror)
plt.ylabel("Raw Value")
plt.xlabel("Time")
plt.show()

plt.title("Reported_Uncorrect")
dates = pltdates.datestr2num(times)
plt.plot_date(dates, repuncorrect)
plt.ylabel("Raw Value")
plt.xlabel("Time")
plt.show()

plt.title("Command_Timeout")
dates = pltdates.datestr2num(times)
plt.plot_date(dates, comtimeout)
plt.ylabel("Raw Value")
plt.xlabel("Time")
plt.show()

plt.title("Airflow_Temperature_Cel")
dates = pltdates.datestr2num(times)
plt.plot_date(dates, airflowtemp)
plt.ylabel("Raw Value")
plt.xlabel("Time")
plt.show()

plt.title("Power-Off_Retract_Count")
dates = pltdates.datestr2num(times)
plt.plot_date(dates, poffretract)
plt.ylabel("Raw Value")
plt.xlabel("Time")
plt.show()

plt.title("Load_Cycle_Count")
dates = pltdates.datestr2num(times)
plt.plot_date(dates, loadcycle)
plt.ylabel("Raw Value")
plt.xlabel("Time")
plt.show()

plt.title("Temperature_Celsius")
dates = pltdates.datestr2num(times)
plt.plot_date(dates, temp)
plt.ylabel("Raw Value")
plt.xlabel("Time")
plt.show()

plt.title("Hardware_ECC_Recovered")
dates = pltdates.datestr2num(times)
plt.plot_date(dates, hweccrec)
plt.ylabel("Raw Value")
plt.xlabel("Time")
plt.show()

plt.title("Reallocated_Event_Count")
dates = pltdates.datestr2num(times)
plt.plot_date(dates, reallocev)
plt.ylabel("Raw Value")
plt.xlabel("Time")
plt.show()

plt.title("Current_Pending_Sector")
dates = pltdates.datestr2num(times)
plt.plot_date(dates, pendingsct)
plt.ylabel("Raw Value")
plt.xlabel("Time")
plt.show()

plt.title("Offline_Uncorrectable")
dates = pltdates.datestr2num(times)
plt.plot_date(dates, offluncorr)
plt.ylabel("Raw Value")
plt.xlabel("Time")
plt.show()

plt.title("UDMA_CRC_Error_Count")
dates = pltdates.datestr2num(times)
plt.plot_date(dates, crcerror)
plt.ylabel("Raw Value")
plt.xlabel("Time")
plt.show()

plt.title("Multi_Zone_Error_Rate")
dates = pltdates.datestr2num(times)
plt.plot_date(dates, mzerror)
plt.ylabel("Raw Value")
plt.xlabel("Time")
plt.show()


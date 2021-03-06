#!/usr/bin/env python3

import os
import sys
import time
import datetime
import matplotlib.pyplot as plt
import matplotlib.dates as pltdates
from matplotlib.backends.backend_pdf import PdfPages
from optparse import OptionParser

# greetings line
version = "1.1"
print("smartplot v" + version + " (c) 2019 Robert Krause <ruport@f00l.de>\n")

# parse options and arguments
parser = OptionParser(usage="usage: %prog [options] <inputfile>")
parser.add_option("-o", "--output", dest="outputfile", help="write report to FILE", metavar="FILE", type="string", default="report.pdf")
parser.add_option("-f", "--format", dest="format", help="choose output format (PDF or PNG)", metavar="format", type="string", default="PDF")
parser.add_option("-e", "--event", dest="event", help="mark event in graphs (format: DD.MM.YYYY-HH:MM", metavar="DATE", type="string", default=None)
parser.add_option("-d", "--days", dest="lastdays", help="only handle last days until today", metavar="DAYS", type="int", default=None)
parser.add_option("-s", "--seagate", dest="seagate", help="interpret values with seagate calculation", action="store_true", default=False)

(options, args) = parser.parse_args()

if len(args) != 1:
  parser.error("input file name missing")

if options.format != "PDF" and options.format != "PNG":
  parser.error("invalid output format")

# set config vars
sourcefile = args[0]

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
          180: "Unused_Reserved_Block_Count_Total",
          183: "Runtime_Bad_Block",
          184: "End-to-End_Error",
          187: "Reported_Uncorrect",
          188: "Command_Timeout",
          189: "High_Fly_Writes",
          190: "Airflow_Temperature_Cel",
          191: "G-Sense_Error_Rate",
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
          225: "Load-Unload_Cycle_Count",
          228: "Power-Off_Retract_Cycle",
          240: "Head_Flying_Hours",
          241: "Total_LBAs_Written",
          242: "Total_LBAs_Read" }

# prepare plot arrays
times = []
data = {}

# calc last day timestamp
if options.lastdays != None:
  tslimit = time.time() - (options.lastdays * 24 * 60 * 60)

# calc event ts
if options.event != None:
  eventts = time.mktime(datetime.datetime.strptime(options.event, "%d.%m.%Y-%H:%M").timetuple())
  if options.lastdays != None and eventts < tslimit:
    print("WARNING: Event date is outside of plot limit.")
  eventobj = datetime.datetime.fromtimestamp(eventts)


# force matlibplot to not use any x backends
plt.switch_backend('agg')

# since smartd uses 2-character-separator (;\t), we need to split ourself
csvfile = open(sourcefile, "r")
while True:
  line = csvfile.readline()
  if len(line) == 0: break

  # split line
  parts = line.split(";\t")
  timeval = parts[0]

  # skip entry if daylimit is not reached
  if options.lastdays != None:
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

    # some hdds give multiple values masked into one raw value
    # to only get the important one (for now), filter those values

    # Airflow_Temperature_Cel (degrees are last 8 bits)
    if id == 190: rawvalue = rawvalue & 0xff
    # Temperature_Celsius (degrees are last 8 bits)
    if id == 194: rawvalue = rawvalue & 0xff
    # Head_Flying_Hours (hours are last 32 bits)
    if id == 240: rawvalue = rawvalue & 0xffffffff

    # SEAGATE
    if options.seagate:
      # raw read error is 48 bits for seagate
      # upper 16 bits are read error counter
      # lower 32 bits are read counter
      if id == 1:
        rawvalue = rawvalue >> 32;

      # seek error is 48 bits for seagate
      # upper 16 bits are seek error counter
      # lower 32 bits are seek counter
      if id == 7:
        rawvalue = rawvalue >> 32;

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
if options.format == "PDF":
  pdf = PdfPages(options.outputfile)

  # fill pdf info data
  info = pdf.infodict()
  info['Title'] = 'Analysis of ' + sourcefile
  info['Author'] = 'smartplot'
  info['Subject'] = 'Analysis of ' + sourcefile
  info['Keywords'] = 'S.M.A.R.T. report by smartplot'
  info['CreationDate'] = datetime.datetime.today()
  info['ModDate'] = datetime.datetime.today()

  # print first info page (PDF only)
  firstPage = plt.figure(figsize=(20,10))
  firstPage.clf()
  firstPage.text(0.05, 0.95, "S.M.A.R.T. report generated by smartplot v" + version + " (https://f00l.de/smartplot/)", transform=firstPage.transFigure, size=24)
  firstPage.text(0.05, 0.85, "Report date: " + str(datetime.datetime.today()), transform=firstPage.transFigure, size=24)
  firstPage.text(0.05, 0.80, "Source file: " + os.path.basename(sourcefile), transform=firstPage.transFigure, size=24)
  firstPage.text(0.05, 0.75, "Analysis time span: " + times[0] + " - " + times[-1], transform=firstPage.transFigure, size=24)
  firstPage.text(0.05, 0.70, "Total number different attribute ids: " + str(len(data)), transform=firstPage.transFigure, size=24)
  firstPage.text(0.05, 0.65, "Total number of data sets per attribute: " + str(len(times)), transform=firstPage.transFigure, size=24)
  if options.event != None:
    firstPage.text(0.05, 0.60, "Configured event on date: " + options.event, transform=firstPage.transFigure, size=24)
  pdf.savefig()
  plt.close()

# plot data
for id in data:
  # get proper id name string
  if id in idstr:
    idname = idstr[id]
  else:
    idname = "Unknown_HDD_Attribute_" + str(id)

  print("Plotting " + idname + "...")

  # prepare figure and subplots
  f, axarr = plt.subplots(2, figsize=(20,10))
  rawplot = axarr[0]
  valplot = axarr[1]

  # plot raw value
  rawplot.set_title(idname + " (RAW_VALUE)")
  dates = pltdates.datestr2num(times)
  rawplot.plot_date(dates, data[id]['raw'], 'black')
  rawplot.set_ylabel("Value")
  rawplot.legend(["Raw Value"])
  if options.event != None:
    rawplot.axvline(x=eventobj, color='r', linestyle='--')

  # plot value
  valplot.set_title(idname + " (VALUE)")
  dates = pltdates.datestr2num(times)
  valplot.plot_date(dates, data[id]['value'], 'b')
  valplot.set_ylabel("Value")
  valplot.legend(["Current Value"])
  if options.event != None:
    valplot.axvline(x=eventobj, color='r', linestyle='--')

  # save figure to pdf or png
  if options.format == "PDF":
    pdf.savefig()
  else:
    plt.savefig("attr-" + str(id) + ".png")
  plt.close(f)

# close pdf file
if options.format == "PDF":
  pdf.close()

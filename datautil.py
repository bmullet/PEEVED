import csv
import matplotlib.pyplot as plt
import numpy as np
import pdb

def load_hypocenters(csv_path):
    """Load dataset from a CSV file.

    Args:
         csv_path: Path to CSV file containing dataset.

    Returns:
        xs: Numpy array of x-values (inputs).
        ys: Numpy array of y-values (labels).
    """

    # Load headers
    with open(csv_path, 'r') as csv_fh:
        headers = csv_fh.readline().strip().split(',')

    # Load features and labels
    tcol   = [i for i in range(len(headers)) if headers[i]=='time']
    latcol = [i for i in range(len(headers)) if headers[i]=='latitude']
    loncol = [i for i in range(len(headers)) if headers[i]=='longitude']
    depcol = [i for i in range(len(headers)) if headers[i]=='depth']
    magcol = [i for i in range(len(headers)) if headers[i]=='mag']

    tTmp = np.loadtxt(csv_path, delimiter=',', skiprows=1, usecols=tcol, dtype='str')
    lat  = np.loadtxt(csv_path, delimiter=',', skiprows=1, usecols=latcol)
    lon  = np.loadtxt(csv_path, delimiter=',', skiprows=1, usecols=loncol)
    depth= np.loadtxt(csv_path, delimiter=',', skiprows=1, usecols=depcol)
    mag  = np.loadtxt(csv_path, delimiter=',', skiprows=1, usecols=magcol)

    # parse the time into something understandable
    Neq  = len(mag)
    time = np.zeros((Neq, 6))
    # year, month, day, hour, min, sec

    for eqi in range(Neq):
        ymd, hms = tTmp[eqi].split('T')

        year,month,day  = ymd.split('-')
        hour,minute,sec = hms.split(':')
        sec,junk        = sec.split('.')

        time[eqi,0] = float(year)
        time[eqi,1] = float(month)
        time[eqi,2] = float(day)
        time[eqi,3] = float(hour)
        time[eqi,4] = float(minute)
        time[eqi,5] = float(sec)

    return time, lat, lon, depth, mag
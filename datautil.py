import csv
import matplotlib.pyplot as plt
import numpy as np
import pdb
from datetime import datetime

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

    ttmp = [s.split('.')[0] for s in tTmp]
    time = [datetime.strptime(tstr, '%Y-%m-%dT%H:%M:%S') for tstr in ttmp]

    return time, lat, lon, depth, mag

def load_puuoo(csv_path):
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

    ncol = headers.index("Number")
    dcol = headers.index("Date")
    repose_col = headers.index("Repose")
    lcol = headers.index("Length")
    facol = headers.index("Flow Area")
    fvcol = headers.index("Flow Volume")
    rcol = headers.index("Rate")
    loccol = headers.index("Location")

    id  = np.loadtxt(csv_path, delimiter=',', skiprows=1, usecols=ncol)

    t = np.loadtxt(csv_path, delimiter=',', skiprows=1, usecols=dcol, dtype='str')
    t = list(t)
    t = [datetime.strptime(val, '%m/%d/%y') for val in t]

    length  = np.loadtxt(csv_path, delimiter=',', skiprows=1, usecols=lcol, dtype='str')
    length = list(length)
    length = np.array([float(val.split(' hrs')[0]) for val in length])

    repose = np.loadtxt(csv_path, delimiter=',', skiprows=1, usecols=repose_col)
    flow_area  = np.loadtxt(csv_path, delimiter=',', skiprows=1, usecols=facol)
    flow_volume = np.loadtxt(csv_path, delimiter=',', skiprows=1, usecols=fvcol)
    rate = np.loadtxt(csv_path, delimiter=',', skiprows=1, usecols=rcol)
    location = np.loadtxt(csv_path, delimiter=',', skiprows=1, usecols=loccol, dtype='str')

    return id, t, length, repose, flow_area, flow_volume, rate, location

class PuuOo:
    def __init__(self, csv_path):
        self.csv_path = csv_path
        id, t, length, repose, flow_area, flow_volume, rate, location = load_puuoo(csv_path)
        self.id = id
        self.dates = t
        self.length = length
        self.repose = repose
        self.flow_area = flow_area
        self.flow_volume = flow_volume
        self.rate = rate
        self.location = location

    def was_erupting(self, time):
        # Find closest event
        event = max([i for i in self.dates if time > i])
        idx = self.dates.index(event)
        event_length = self.length[idx]

        # Get time difference
        time_diff = time - event
        timediff_hours = time_diff.days*24 + time_diff.seconds/3600

        # give a 24h buffer window because we aren't sure the time of the eruption
        return timediff_hours < event_length + 24


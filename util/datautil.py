import csv
import matplotlib.pyplot as plt
import numpy as np
import pdb
from itertools import compress
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

def load_puuoo_eqs(csv_path):
    """
    Load wovodat PuuOo csv
    :param
        csv_path: path to csv
    :return
        data arrays
    """
    # Load headers
    with open(csv_path, 'r') as csv_fh:
        headers = csv_fh.readline().strip().split(',')

    # Load features and labels
    tcol   = [i for i in range(len(headers)) if headers[i]=='Date-time']
    latcol = [i for i in range(len(headers)) if headers[i]=='Latitude']
    loncol = [i for i in range(len(headers)) if headers[i]=='Longitude']
    depcol = [i for i in range(len(headers)) if headers[i]=='Depth']
    magcol = [i for i in range(len(headers)) if headers[i]=='Magnitude']

    tTmp = np.loadtxt(csv_path, delimiter=',', skiprows=1, usecols=tcol, dtype='str')
    lat  = np.loadtxt(csv_path, delimiter=',', skiprows=1, usecols=latcol)
    lon  = np.loadtxt(csv_path, delimiter=',', skiprows=1, usecols=loncol)
    depth= np.loadtxt(csv_path, delimiter=',', skiprows=1, usecols=depcol)
    mag  = np.loadtxt(csv_path, delimiter=',', skiprows=1, usecols=magcol)

    ttmp = [s.split('.')[0] for s in tTmp]
    time = [datetime.strptime(tstr, '%m/%d/%Y %H:%M:%S') for tstr in ttmp]

    return time, lat, lon, depth, mag


def load_puuoo_eruptions(csv_path):
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


def prune_data(time, lat, lon, depth, mag, puuoo):
    """
    Prune data by removing all eqs that happened before eruption catalogue starts
    WARNING: be careful with datatypes (assumes you want list for time and numpy array for other vars)
    """

    idx = [puuoo.was_erupting(t) is not None for t in time]
    
    time  = list(compress(time, idx))
    lat   = np.array(list(compress(lat, idx)))
    lon   = np.array(list(compress(lon, idx)))
    depth = np.array(list(compress(depth, idx)))
    mag   = np.array(list(compress(mag, idx)))
    
    return time, lat, lon, depth, mag

def GetTimeToEruption (EQtime, p):
    """
    For each earthquake, determine the time TO eruption in seconds. 
    If you want it in other units, just convert outside the function.
    """
    
    SecsToEruption = np.zeros(len(EQtime))

    for di in range(len(EQtime)):

        NextEruptions = [i for i in p.dates if i>EQtime[di]]

        if p.was_erupting(EQtime[di]):
            SecsToEruption[di] = 0

        elif not NextEruptions:
            SecsToEruption[di] = np.nan

        else:        
            timediff = NextEruptions[0] - EQtime[di]
            SecsToEruption[di] = timediff.days*24*3600 + timediff.seconds
            
    
    return SecsToEruption

def GetTimeSinceEruption (EQtime, p):
    """
    For each earthquake, determine the time SINCE eruption in seconds. 
    If you want it in other units, just convert outside the function.
    """
    
    SecsSinceEruption = np.zeros(len(EQtime))
    t0 = datetime(1982, 9, 25)  # time of previous eruption at Halemaumau
    
    for di in range(len(EQtime)):
        PrevEruption = [i for i in p.dates if EQtime[di]>i]
        
        if p.was_erupting(EQtime[di]):
            SecsSinceEruption[di] = 0

        elif not PrevEruption:
            timediff = EQtime[di] - t0
            SecsSinceEruption[di] = timediff.days*24*3600 + timediff.seconds

        else:        
            PrevEruptionIndex = p.dates.index(PrevEruption[-1])
            timediff = EQtime[di] - PrevEruption[-1]
            SecsSinceEruption[di] = timediff.days*24*3600 + timediff.seconds - p.length[PrevEruptionIndex]*3600
            
    return SecsSinceEruption

def GetEQRates (EQtime):
    """
    Returns the number of earthquakes in the 
    last day, last week (7 days) and last month (30 days) 
    leading up to each earthquake
    """
    
    EQsLastDay   = np.zeros(len(EQtime))
    EQsLastWeek  = np.zeros(len(EQtime))
    EQsLastMonth = np.zeros(len(EQtime))
    
    for di in range(len(EQtime)):
        timediff = [EQtime[di] - EQtime[ti] for ti in range(len(EQtime))]
        
        EQsLastDay[di]   = len([i for i in range(len(EQtime)) if timediff[i].days==0 and EQtime[di]>EQtime[i]])
        EQsLastWeek[di]  = len([i for i in range(len(EQtime)) if timediff[i].days<=7 and timediff[i].days>=0 and EQtime[di]>EQtime[i]])
        EQsLastMonth[di] = len([i for i in range(len(EQtime)) if timediff[i].days<=30 and timediff[i].days>=0 and EQtime[di]>EQtime[i]])
    
    return EQsLastDay, EQsLastWeek, EQsLastMonth









class PuuOo:
    def __init__(self, csv_path):
        self.csv_path = csv_path
        id, t, length, repose, flow_area, flow_volume, rate, location = load_puuoo_eruptions(csv_path)
        self.id = id
        self.dates = t
        self.length = length
        self.repose = repose
        self.flow_area = flow_area
        self.flow_volume = flow_volume
        self.rate = rate
        self.location = location

    def was_erupting(self, time, verbose=False):
        # Find closest event
        try:
            event = max([i for i in self.dates if time > i])
            idx = self.dates.index(event)
            event_length = self.length[idx]

            # Get time difference
            time_diff = time - event
            timediff_hours = time_diff.days*24 + time_diff.seconds/3600

            # give a 24h buffer window because we aren't sure the time of the eruption
            return timediff_hours < event_length + 24

        except:
            if verbose:
                print(f'Time {str(time)} is before eruption history begins')
                return None
            else:
                return None

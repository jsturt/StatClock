import pandas as pd
import numpy as np

"""

Want to turn this file into a set of clean routines that can be called from 
another main py file with arguments such as player name, filepath etc. 

This means that unique "main" files can be created for different tasks / the
analysis and reporting is kept separate from the bare utility and calculation 
code.

"""

def initialize(name,filepath):
    name = 'nine inch whales'
    start = name + ' connected' 
    
    # Open File
    with open('spydata.txt', encoding="utf8") as f:
        data = f.readlines()
    f.close()
    
    # Remove new line characters
    data = [dat.strip(f'\n') for dat in data]
    
    # Remove chat messages in case, if want to isolate msgs remove 'not'
    data2 = [dat for dat in data if not (' : ' in dat.replace(name,''))]
    
    # Find locations of connection events
    for loc,line in enumerate(reversed(data)):
        if(line==start):
            loc=len(data)-loc-1
            break
        else:
            continue
    
    # Strips out all but the last game connected to
    data = data[loc:]
    
    # Find kill events
    tailored = [dat for dat in data if (name in dat and 'killed' in dat)]

    # find word after 'with' aka the weapon.
    [tailored[1].split()[i+1] for i,word in enumerate(tailored[1].split()) if word == 'with']
    
    kdList = [categorise(name,val) for val in tailored]    
    weapons = [weapon(line) for line in tailored]
    crits = [crit(line) for line in tailored]
    player2 = [removeClutter(line,name) for line in tailored]
    
    df = pd.DataFrame(
        {'k/d': kdList,
         'player2': player2,
         'weapon': weapons,
         'crit': crits
        })
        
    pd.set_option('display.max_columns', None)
    return df


def categorise(player,line):
    """
    Categorise lines as player kills or player deaths
    """
    # Determine where the player name occurs
    for i,val in enumerate(line):
        if player in line[:i]:
            idx = i
            break
        else:
            idx = len(line)
            
    # If the next word is with, the line is a death message
    if(line[idx+1:idx+5] == 'with'):
        return 'death'
    else:
        return 'kill'
       
def removeClutter(line,name):
    """
    Extracts player2 name from line
    """    
    line = line.replace(name,'',1)
    line = line.replace(' (crit)','',1)
    line = line.replace(weapon(line)+'.','',1)
    line = line.replace(' with ','')
    line = line.replace(' killed ','')
    return line


def killCount(dataframe):
    """
    Returns # of kills
    """
    return dataframe['k/d'].value_counts().kill

def deathCount(dataframe):
    """
    Returns # of deaths
    """
    return dataframe['k/d'].value_counts().death

def kd(dataframe):
    """
    Calculates k/d ratio to 3 dp
    """
    return round(killCount(dataframe)/deathCount(dataframe),3)

def weapon(line):
    """
    Finds weapon out of event lines
    """
    return str([line.split()[i+1] for i,word in enumerate(line.split()) if word == 'with']).strip("[]'.")

def crit(line):
    """
    Check if event was caused by a crit.
    """
    return line.split()[-1] == '(crit)'

def killedBy(dataframe):
    """
    Returns lists of weapons died to in order of occurance
    """
    return dataframe.loc[(dataframe['k/d'] == 'death') , ['weapon'] ]
    
def killedByWeapon(dataframe,cause):
    """
    Returns list of deaths to certain weapon in order of occurance
    """
    return dataframe.loc[(dataframe['k/d'] == 'death') & (dataframe['weapon'] == cause), ['weapon']]

def killsWith(dataframe):
    """
    Returns list of kills in order of occurance
    """
    return dataframe.loc[(dataframe['k/d'] == 'kill') , ['weapon'] ]    

def killsWithWeapon(dataframe,cause):
    """
    Returns list of kills with a certain weapon in order of occurance
    """
    return dataframe.loc[(dataframe['k/d'] == 'kill') & (dataframe['weapon'] == cause), ['weapon']]

def numKillsWithWeapon(dataframe,cause):
    """
    Returns number of kills with a weapon
    """
    return killsWithWeapon(dataframe,cause)['weapon'].value_counts()[0]

def numKilledByWeapon(dataframe,cause):
    """
    Returns number of kills with a weapon
    """
    return killedByWeapon(dataframe,cause)['weapon'].value_counts()[0]

def mostKillsWith(dataframe):
    """
    Returns weapon with most kills
    """
    val = dataframe.loc[(dataframe['k/d'] == 'kill') ,  ]['weapon'].value_counts()
    return (val.index[0],val[0])

def mostKilledBy(dataframe):
    """
    Returns the weapon most killed by
    """
    val = dataframe.loc[(dataframe['k/d'] == 'death') ,  ]['weapon'].value_counts()
    return (val.index[0],val[0])

def killstreaks(dataframe):
    """
    Returns list of killstreaks found
    """
    kCount = 0
    ksList = [] # list of killstreaks
    for index,row in dataframe.iterrows():
        if(row['k/d'] == 'kill'):   # can filter by weapon here if wanted, i.e. only track kills with 'kunai' by "and row['weappon']=='kunai'"
            kCount += 1
        else:
            ksList.append(kCount)
            kCount = 0
    return ksList 


def stdKills(dataframe):
    """
    Returns the standard deviation of kills per death
    - kd is the sample mean, stdKills quantifies its variability within the sample
    """
    ks = killstreaks(dataframe)
    kdr = kd(dataframe)
    variance = sum([ (elem - kdr)**2 for elem in ks ]) / (len(ks)-1)
    return variance**0.5


"""

TODO:   Allow for analysis of k/d and stddev of a particular weapon rather than the whole sample
        Filtering by team switching
        Pickling logs for long-term analysis.

Aim:
    Save and load past dataframes to track trends over time
        Name pickles by date/time/map?
        Load pickles by range of dates ?
    
    Histograms for weapons user dies to or kills with most?
    Want to be able to plot what I'm killed by and what I kill with
    Have legends automatically assigned based upon the weapon used

    Track values over time - need data structure (pandas saving?) to accomplish this
    Make histograms of weapon kill freq per game?
    Weapons die most to / Kill most with
    Track suicides "name + 'suicided.'"
    
Whats needed for this goal:
    Handle when names contain 'killed with'
    Track when last death was
    Track when die to certain weapons
    Remove lines that contain colons outside of the name to eliminate chat interference
    i.e. someone may say 'idiot : I killed nine inch whales'
        need to make sure BOTH names dont have colons
        '. : idiot : . killed nine inch whales with ... '
        'nine inch whales killed . : idiot : . with ... '
        want to remove lines that have colons outside of the names


Problems:
    If someones name contains any of the flags that are used to find locations in the file then the program will not work
        Find a way to mitigate this
        => Look for chunks of text that indicate connection rather than connected etc
"""  

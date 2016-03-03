import numpy as np
import csv
syear=2003
eyear=2016

def load_data(filename):
    mat=[]
    with open(filename, 'rb') as csvfile:
        spamreader = csv.reader(csvfile, delimiter=',')
        for row in spamreader:
            mat.append(row)

    return mat

def load_data_num(filename):
    data = np.genfromtxt(filename, dtype=float, delimiter=',', names=True)
    return data

def compile_team_metrics(seasons):
    # get list of teams - only need teams from win
    teams=np.unique(seasons['Wteam'])
    team_stats={}
    team_stats=calc_wins(seasons,team_stats,teams)
    return team_stats

def calc_wins(seasons,team_stats,teams):
    #prepopulate dict keys
    years=range (syear,eyear)
    for year in years:
        for team in teams:
            if team not in team_stats.keys():
                team_stats[team]={}
            if year not in team_stats[team].keys():
                team_stats[team][year]={}
    #create a numpy matrix for each team/year key
    team_statmat=np.zeros([len(range(syear,eyear))*len(teams),50])
    c=0
    for year in range (syear,eyear):
        for team in teams:
            #print team_stats
            team_stats[team][year]['wins']=len(seasons[(np.where((seasons['Wteam']==team) & (seasons['Season'] ==year)))])
            team_stats[team][year]['avgptsw']=np.mean((seasons[(np.where((seasons['Wteam']==team) & (seasons['Season'] ==year)))]['Wscore']))
            team_stats[team][year]['avgptsl']=np.mean((seasons[(np.where((seasons['Lteam']==team) & (seasons['Season'] ==year)))]['Lscore']))
            team_statmat[c,0]=team
            team_statmat[c,1]=year
            team_statmat[c,2]=len(seasons[(np.where((seasons['Wteam']==team) & (seasons['Season'] ==year)))])
            team_statmat[c,3]=np.mean((seasons[(np.where((seasons['Wteam']==team) & (seasons['Season'] ==year)))]['Wscore']))
            team_statmat[c,4]=np.mean((seasons[(np.where((seasons['Lteam']==team) & (seasons['Season'] ==year)))]['Lscore']))
            c+=1
    np.savetxt("teamyear.csv", team_statmat, delimiter=",")
    return team_statmat





def main():
    datadir='march-machine-learning-mania-2016-v1/'

    #season data
    #Season,Daynum,Wteam,Wscore,Lteam,Lscore,Wloc,Numot,Wfgm,Wfga,Wfgm3,Wfga3,Wftm,Wfta,Wor,Wdr,Wast,Wto,Wstl,Wblk,Wpf,Lfgm,Lfga,Lfgm3,Lfga3,Lftm,Lfta,Lor,Ldr,Last,Lto,Lstl,Lblk,Lpf
    seasons=load_data_num(datadir+'RegularSeasonDetailedResults.csv')
    teams=load_data(datadir+'Teams.csv')
    teamstats=compile_team_metrics(seasons)

    print teamstats
    #print seasons[np.where(seasons['Wteam']==1104)]
if '__name__'!='main':
    main()
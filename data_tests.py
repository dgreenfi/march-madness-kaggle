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
    #create numpy matrix for population
    team_statmat=np.zeros([len(range(syear,eyear))*len(teams),50])
    c=0
    for year in range (syear,eyear):
        for team in teams:
            ############   Team Level Stats
            team_statmat[c,0]=team
            team_statmat[c,1]=year
            # count of wins
            team_statmat[c,2]=len(seasons[(np.where((seasons['Wteam']==team) & (seasons['Season'] ==year)))])
            #mean pts in wins
            team_statmat[c,3]=np.mean((seasons[(np.where((seasons['Wteam']==team) & (seasons['Season']==year)))]['Wscore']))
            #mean pts in losses
            team_statmat[c,4]=np.mean((seasons[(np.where((seasons['Lteam']==team) & (seasons['Season']==year)))]['Lscore']))
            #margin of victory in wins
            team_statmat[c,5]=np.mean((seasons[(np.where((seasons['Wteam']==team) & (seasons['Season']==year)))]['Wscore'])-np.mean((seasons[(np.where((seasons['Wteam']==team) & (seasons['Season'] ==year)))]['Lscore'])))
            #margin of loss in losses
            team_statmat[c,6]=np.mean((seasons[(np.where((seasons['Lteam']==team) & (seasons['Season']==year)))]['Lscore'])-np.mean((seasons[(np.where((seasons['Lteam']==team) & (seasons['Season'] ==year)))]['Wscore'])))
            #avg fgmade wins
            team_statmat[c,7]=np.mean((seasons[(np.where((seasons['Wteam']==team ) & (seasons['Season']==year)))]['Wfgm']))
            #avg fg attempted wins
            team_statmat[c,8]=np.mean((seasons[(np.where((seasons['Wteam']==team ) & (seasons['Season']==year)))]['Wfga']))
            #avg fgmade losses
            team_statmat[c,9]=np.mean((seasons[(np.where((seasons['Lteam']==team ) & (seasons['Season']==year)))]['Lfgm']))
            #avg fg attempted losses
            team_statmat[c,10]=np.mean((seasons[(np.where((seasons['Lteam']==team ) & (seasons['Season']==year)))]['Lfga']))
            #avg 3pt made wins
            team_statmat[c,11]=np.mean((seasons[(np.where((seasons['Wteam']==team ) & (seasons['Season']==year)))]['Wfgm3']))
            #avg 3pt attempted wins
            team_statmat[c,12]=np.mean((seasons[(np.where((seasons['Wteam']==team ) & (seasons['Season']==year)))]['Wfgm3']))
            #avg 3pt made losses
            team_statmat[c,13]=np.mean((seasons[(np.where((seasons['Lteam']==team ) & (seasons['Season']==year)))]['Lfgm3']))
            #avg 3pt attempted losses
            team_statmat[c,14]=np.mean((seasons[(np.where((seasons['Lteam']==team ) & (seasons['Season']==year)))]['Lfgm3']))

            ##########Opponent statistics##########
            # need a different appliance since opponent stats will have to grab a game set for each opponent team and not 1 team

            #record iterator
            c+=1
    np.savetxt("teamyear.csv", team_statmat, delimiter=",")
    return team_statmat





def main():
    derive_team_stats=1
    datadir='march-machine-learning-mania-2016-v1/'

    #season data
    #Season,Daynum,Wteam,Wscore,Lteam,Lscore,Wloc,Numot,Wfgm,Wfga,Wfgm3,Wfga3,Wftm,Wfta,Wor,Wdr,Wast,Wto,Wstl,Wblk,Wpf,Lfgm,Lfga,Lfgm3,Lfga3,Lftm,Lfta,Lor,Ldr,Last,Lto,Lstl,Lblk,Lpf
    seasons=load_data_num(datadir+'RegularSeasonDetailedResults.csv')
    teams=load_data(datadir+'Teams.csv')
    if derive_team_stats==1:
        teamstats=compile_team_metrics(seasons)


    #print seasons[np.where(seasons['Wteam']==1104)]
if '__name__'!='main':
    main()
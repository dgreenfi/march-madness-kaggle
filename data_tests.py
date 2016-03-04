import numpy as np
import csv
import networkx as nx
import pandas as pd
syear=2003
eyear=2016
years=range(syear,eyear)

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
    team_statmat=np.zeros([len(range(syear,eyear))*len(teams),17])
    c=0
    names=['team','year','wins','winscore','lossscore','mvic','mloss','wfgm','wfga','lfgm','lfga','wfgm3','wfga3','lfga3','lfgm3','pr','pr_w']
    #index by team year key
    index_df=[]
    for year in range (syear,eyear):
        for team in teams:
            index_df.append(str(int(team))+str(year))

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
            team_statmat[c,12]=np.mean((seasons[(np.where((seasons['Wteam']==team ) & (seasons['Season']==year)))]['Wfga3']))
            #avg 3pt made losses
            team_statmat[c,13]=np.mean((seasons[(np.where((seasons['Lteam']==team ) & (seasons['Season']==year)))]['Lfgm3']))
            #avg 3pt attempted losses
            team_statmat[c,14]=np.mean((seasons[(np.where((seasons['Lteam']==team ) & (seasons['Season']==year)))]['Lfga3']))

            ##########Opponent statistics##########
            # need a different appliance since opponent stats will have to grab a game set for each opponent team and not 1 team

            #record iterator
            c+=1

    team_statmat_df = pd.DataFrame(team_statmat, index=index_df, columns=names)
    #np.savetxt("teamyear.csv", team_statmat, delimiter=",")
    return team_statmat_df


def create_schedule_graph(seasons,teams):
    #let's create a directional graph of teams who played each other so we can create a Page rank
    #teams =[t[1] for t in teams[1:]]
    t_lookup={int(t[0]):t[1] for t in teams[1:]}
    print teams
    teams =[int(t[0]) for t in teams[1:]]
    pr_hist={}
    pr_w_hist={}
    for year in years:
        G=nx.DiGraph()
        G.add_nodes_from(teams)
        G_w=G.copy()
        games=seasons[np.where((seasons['Season']==year))]

        for game in games:
            #add a directional endorsement from the losing team to winning team
            G.add_weighted_edges_from([(game['Lteam'],game['Wteam'],1)])
            # weight by win % squared
            G_w.add_weighted_edges_from([(game['Lteam'],game['Wteam'],(game['Wscore']/game['Lscore'])**2)])
        pr=nx.pagerank(G, alpha=0.9)
        pr_w=nx.pagerank(G_w, alpha=0.9)
        ranks=[]
        ranks_w=[]
        for r in pr:
            ranks.append((t_lookup[r],pr[r]))
        for r in pr_w:
            ranks_w.append((t_lookup[r],pr_w[r]))
        pr_hist[year]=pr
        pr_w_hist[year]=pr_w
    sorted_pr = sorted(ranks, key=lambda tup: tup[1],reverse=True)
    sorted_pr_w = sorted(ranks_w, key=lambda tup: tup[1],reverse=True)
    return pr_hist,pr_w_hist

def append_ranks(mat,pr,colname):

    for year in pr.keys():
        for team in pr[year].keys():
            #print pr[year][team]*10000
            if str(team)+str(year) in mat.axes[0]:
                mat[colname][str(team)+str(year)]=pr[year][team]*100
                #print colname,str(team)+str(year),pr[year][team]*100

    return mat

def assemble_train_mat(teamstats,tourneyseeds,tourneyslots,tourneyresults,targetyear):
    #assemble matrix X of teamA,TeamB,stat1,stat2...statn,opponentstat and array of vectors y of result, teamascore,teambscore



def main():
    derive_team_stats=1
    datadir='march-machine-learning-mania-2016-v1/'

    #season data
    #Season,Daynum,Wteam,Wscore,Lteam,Lscore,Wloc,Numot,Wfgm,Wfga,Wfgm3,Wfga3,Wftm,Wfta,Wor,Wdr,Wast,Wto,Wstl,Wblk,Wpf,Lfgm,Lfga,Lfgm3,Lfga3,Lftm,Lfta,Lor,Ldr,Last,Lto,Lstl,Lblk,Lpf
    seasons=load_data_num(datadir+'RegularSeasonDetailedResults.csv')
    teams=load_data(datadir+'Teams.csv')
    tourneyresults=load_data(datadir+'TourneyCompactResults.csv')
    tourneyseeds=load_data(datadir+'TourneySeeds.csv')
    tourneyslots=load_data(datadir+'TourneySlots.csv')
    pr,pr_w=create_schedule_graph(seasons,teams)
    #print pr

    if derive_team_stats==1:
        teamstats=compile_team_metrics(seasons)

    teamstats=append_ranks(teamstats,pr,'pr')
    teamstats=append_ranks(teamstats,pr_w,'pr_w')
    teamstats.to_csv('teamyear.csv', index=True, header=True, sep=',')

    assemble_train_mat(teamstats,tourneyseeds,tourneyslots,tourneyresults,2015)
    #print teamstats
    #print seasons[np.where(seasons['Wteam']==1104)]
if '__name__'!='main':
    main()
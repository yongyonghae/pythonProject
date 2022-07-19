import requests as requests
import pandas as pd
from tqdm import tqdm


def set_api_key(k):
    global key
    key = k


def get_puuid(user):
    url = 'https://kr.api.riotgames.com/lol/summoner/v4/summoners/by-name/' + user + '?api_key=' + key
    res = requests.get(url).json()
    puuid = res['puuid']
    return puuid


def get_matchid(puuid: str, num: int) -> list:
    url = 'https://asia.api.riotgames.com/lol/match/v5/matches/by-puuid/' + puuid + '/ids?start=0&count=' + str(
        num) + '&api_key=' + key
    res = requests.get(url).json()
    lst = list(res)
    return lst


# def get_matches_timelines(matchids):
#     lst = []
#     for matchid in matchids:
#         tmp = []
#         url = 'https://asia.api.riotgames.com/lol/match/v5/matches/' + matchid + '?api_key=' + key
#         res1 = requests.get(url).json()
#         url = 'https://asia.api.riotgames.com/lol/match/v5/matches/' + matchid + '/timeline?api_key=' + key
#         res2 = requests.get(url).json()
#         tmp.append([matchid, res1, res2])
#         lst.extend(tmp)
#     df = pd.DataFrame(lst, columns=['gameId', 'matches', 'timeline'])
#     return df

def get_matches_timelines(matchids):
    lst = []
    for matchid in tqdm(matchids):
        url = 'https://asia.api.riotgames.com/lol/match/v5/matches/' + matchid + '?api_key=' + key
        res1 = requests.get(url).json()
        url = 'https://asia.api.riotgames.com/lol/match/v5/matches/' + matchid + '/timeline?api_key=' + key
        res2 = requests.get(url).json()
        lst.append([matchid, res1, res2])
    return lst


# 승준 추가 220630

import time
from random import sample
import random


def get_rawData(tier):
    div_list = ['I', 'II', 'III', 'IV']
    lst = []
    pageNo = random.randrange(1, 10)

    for d in tqdm(div_list):
        url2 = 'https://kr.api.riotgames.com/lol/league/v4/entries/RANKED_SOLO_5x5/' + tier + '/' + d + '?page=' + \
               str(pageNo) + '&api_key=' + key
        res2 = requests.get(url2).json()
        lst += sample(res2, 5)

    # riot api -> summonerName 가져오기
    lst_dia = [x['summonerName'] for x in lst]

    lst2 = []
    for s in tqdm(lst_dia[:5]):
        # summonerName을 통해서 puuid 가져오기
        try:
            puuid3 = get_puuid(s)
        except Exception as e:
            print(e)

    # match_ids 가져오기
    match_ids = get_matchid(puuid3, 3)

    matches_timeline_list = get_matches_timelines(match_ids)

    # match.timeline 원시데이터 df 만들기
    df = pd.DataFrame(matches_timeline_list, columns=['match_id', 'matches', 'timeline'])
    return df


def get_dataframe_from_game_data(df):
    tmp_lst2 = []
    for h in tqdm(range(len(df))):

        info1 = df.iloc[h].matches['info']
        info2 = df.timeline[h]['info']

        if info1['gameMode'] == 'CLASSIC':
            for i in range(10):
                try:
                    tmp_lst = [
                        info1['gameId'],
                        info1['gameDuration'],
                        info1['gameVersion'],
                        info1['participants'][i]['summonerName'],
                        info1['participants'][i]['summonerLevel'],
                        info1['participants'][i]['participantId'],
                        info1['participants'][i]['championName'],
                        info1['participants'][i]['champExperience'],
                        info1['participants'][i]['teamPosition'],
                        info1['participants'][i]['teamId'],
                        info1['participants'][i]['win'],
                        info1['participants'][i]['kills'],
                        info1['participants'][i]['deaths'],
                        info1['participants'][i]['assists'],
                        info1['participants'][i]['totalDamageDealtToChampions'],
                        info1['participants'][i]['totalDamageTaken'],
                        info1['participants'][i]['baronKills'],
                        info1['participants'][i]['challenges']['teamElderDragonKills'],
                        info1['participants'][i]['dragonKills'],
                        info1['participants'][i]['challenges']['teamRiftHeraldKills']
                    ]
                    for j in range(5, 26):
                        try:
                            tmp_lst.append(info2['frames'][j]['participantFrames'][str(i + 1)]['totalGold'])
                        except:
                            tmp_lst.append(0)
                    tmp_lst2.append(tmp_lst)
                except:
                    continue

    df2 = pd.DataFrame(tmp_lst2, columns=['gameId', 'gameDuration', 'gameVersion', 'summonerName', 'summonerLevel',
                                          'participantId', 'championName', 'champExperience', 'teamPosition', 'teamId',
                                          'win', 'kills', 'deaths', 'assists', 'totalDamageDealtToChampions',
                                          'totalDamageTaken', 'baronKills', 'teamElderDragonKills', 'dragonKills' ,'teamRiftHeraldKills',
                                          'g_5', 'g_6', 'g_7', 'g_8', 'g_9', 'g_10',
                                          'g_11', 'g_12', 'g_13', 'g_14', 'g_15', 'g_16', 'g_17', 'g_18',
                                          'g_19', 'g_20', 'g_21', 'g_22', 'g_23', 'g_24', 'g_25'])
    result_df = df2.drop_duplicates()
    print('complete! the number of df is %d' % len(df))
    return result_df

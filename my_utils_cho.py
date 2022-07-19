import cx_Oracle
import pandas as pd
import requests
from tqdm import tqdm

dsn = cx_Oracle.makedsn('localhost', 1521, 'xe')


def db_open():
    global db
    global cursor
    try:
        cx_Oracle.init_oracle_client(lib_dir=r"C:\oraclexe\app\oracle\instantclient_21_6")
        db = cx_Oracle.connect(user='ADMIN', password='Zhskstkfkd0!',dsn='db20220623152034_high')
        cursor = db.cursor()
        print('open!')
    except :
        db = cx_Oracle.connect(user='ADMIN', password='Zhskstkfkd0!',dsn='db20220623152034_high')
        cursor = db.cursor()
        print('open!')


def db_open_local():
    global db
    global cursor
    db = cx_Oracle.connect(user='JUN', password='1111', dsn=dsn)
    cursor = db.cursor()
    print('open!')


def sql_execute(q):
    global db
    global cursor
    try:
        if 'select' in q:
            df = pd.read_sql(sql=q, con=db)
            return df
        cursor.execute(q)
        return 'success!'
    except Exception as e:
        print(e)


def db_close():
    global db
    global cursor
    try:
        db.commit()
        cursor.close()
        db.close()
        return 'close!'
    except Exception as e:
        print(e)


def df_creater(url):
    api_key = '6269496646616e7438304d5a596156'
    url = url.replace('(인증키)', api_key).replace('xml', 'json').replace('/5/', '/1000/')
    res = requests.get(url).json()
    key = list(res.keys())[0]
    data = res[key]['row']
    df = pd.DataFrame(data)
    return df


def make_sql_of_create(df):
    lst = df.keys()
    tmp = "create table "
    table_name = input("Table name?")
    tmp += table_name
    tmp += '('
    for s in lst:
        question = input("type of " + s + "? (1.varchar, 2.number)")
        if question == '1':
            question = "varchar"
        else:
            question = "number"
        question2 = input("length of " + s + "_" + question + "? (no)")
        tmp += s
        tmp += " "
        tmp += question
        tmp += "("
        tmp += question2
        tmp += ")"
        if s == lst[len(lst) - 1]:
            tmp += ")"
        else:
            tmp += ","

    return tmp


def insert_match_timeline_of(row):
    query = (
        f'merge into match_data_take using dual on(gameId=\'{row.gameId}\' and participantId={row.participantId}) '
        f'when not matched then '
        f'insert(gameId,participantId,gameDuration,gameVersion,summonerName,summonerLevel,championName,'
        f'champExperience,teamPosition,teamId,win,kills,deaths,assists,totalDamageDealtToChampions,totalDamageTaken,'
        f'baronKills,teamElderDragonKills,dragonKills,teamRiftHeraldKills,'
        f'g_5,g_6,g_7,g_8,g_9,g_10,g_11,g_12,g_13,g_14,g_15,g_16,g_17,g_18,g_19,g_20,g_21,g_22,g_23,g_24,g_25) '
        f'values(\'{row.gameId}\',{row.participantId},{row.gameDuration},\'{row.gameVersion}\', \'{row.summonerName}\',{row.summonerLevel},' 
        f'\'{row.championName}\',{row.champExperience},\'{row.teamPosition}\',{row.teamId},\'{row.win}\',{row.kills},'
        f'{row.deaths},{row.assists},{row.totalDamageDealtToChampions},{row.totalDamageTaken},{row.baronKills},'
        f'{row.teamElderDragonKills},{row.dragonKills},{row.teamRiftHeraldKills},{row.g_5},{row.g_6},{row.g_7},{row.g_8},{row.g_9},{row.g_10},'
        f'{row.g_11},{row.g_12},{row.g_13},{row.g_14},{row.g_15},{row.g_16},{row.g_17},{row.g_18},{row.g_19},'
        f'{row.g_20},{row.g_21},{row.g_22},{row.g_23},{row.g_24},{row.g_25})'
    )
    sql_execute(query)
    return


def insert_into_match_data(x):
    tqdm.pandas()
    x.progress_apply(lambda a: insert_match_timeline_of(a), axis=1)
    return


def data_insert(x):
    query2=(
        f'merge into rank_data using dual on(gameId=\'{x.gameId}\' and participantId={x.participantId}) '
        f'when not matched then '
        f'insert (gameId,gameDuration,gameVersion,summonerName ,participantId,championName, '
        f'lane,teamId,win,kills,deaths, assists,damageDealt,damageTaken,bans,killerId,victimId, '
        f'assistId, gold_5_35,firstLaneTower,laneTower,timeLaneTower,g15,Iv6_time) '
        f'values(\'{x.gameId}\',{x.gameDuration},\'{x.gameVersion}\', \'{x.summonerName}\', ' 
        f'\'{x.participantId}\',\'{x.championName}\',\'{x.lane}\',{x.teamId},\'{x.win}\',{x.kills}, '
        f'{x.deaths},{x.assists},{x.damageDealt},{x.damageTaken},\'{x.bans}\',\'{x.killerId}\',\'{x.victimId}\',\'{x.assistId}\', '
        f'\'{x.gold_5_35}\',\'{x.firstLaneTower}\',\'{x.laneTower}\',{x.timeLaneTower},{x.g15},{x.Iv6_time}) '
        )
    sql_execute(query2)
    return



from twpoint.models import Application, WayPoint, statics
import sqlite3
import util
import pdb
#############################################
################### SETUP ###################
#############################################


def connect():
    return sqlite3.connect('./db.sqlite3')


def makeDB():
    con = connect()
    cursor = con.cursor()

    #Make Table
    cursor.execute("CREATE TABLE picture(name varchar(255), path varchar(255), time int, device varchar(255), long real, lat real, md5 varchar(32), sha1 varchar(40));")
    cursor.execute("CREATE TABLE data(appName varchar(255), packageName   varchar(255), path varchar(255), tableName varchar(255), time varchar(255), position varchar(255), positionX varchar(255), positionY varchar(255), start varchar(255), startX varchar(255), startY varchar(255), end varchar(255), endX varchar(255), endY varchar(255), search varchar(255), searchX varchar(255), searchY varchar(255));")
    cursor.execute("CREATE TABLE bs(time int, long real, lat real, sender char(255), reciver char(255), location char(255), type char(255));")
    con.commit()
    con.close()

#############################################
#################### ING ####################
#############################################

################# CONNECT ###################


def inputResDB(insertQuery):
    con = connect()
    cursor = con.cursor()
    cursor.execute(insertQuery)
    con.commit()
    con.close()


def appdata():
    return sqlite3.connect('./appinfo.db')


def appdbconnect(packageName, path, filelocation):
    file_path = filelocation + '/data/' + packageName + '/' + path
    # pdb.set_trace()
    open(file_path, 'rb').read()
    return sqlite3.connect(file_path)

################## GEN #####################


def appQuery(appInfo, appRecord, values):
    query = 'insert into data(appName, packageName, path, tableName, '
    for i in values:
        query = query + i + ", "
    query = query[:-2] + ") values('%s', '%s', '%s', '%s', " % (appInfo['appName'], appInfo['packageName'], appInfo['path'], appInfo['tableName'])
    for i in appRecord:
        query = query + "'%s'," % util.toString(i).replace(u'\'', u'')
    query = query[:-1] + ');'
    return query


def genQuery(record):
    query = "select "
    values = []
    for i in list(record.keys())[4:-1]:
        query = query + record[i] + ","
        values.append(i)
    return query[ :-1] + ' from ' + record['tableName'], values


################# Insert ###################
def writeImageData(name, path, time, device, long, lat, md5, sha1):
    con = connect()
    cursor = con.cursor()
    #insert data
    cursor.execute("INSERT INTO picture VALUES ('%s', '%s', %d, '%s', %0.6lf, %0.6lf, '%s', '%s');" %(name, path, time, device, long, lat, md5, sha1))
    con.commit()
    con.close()

#############################################
#################### END ####################
#############################################


def appDataCount():
    con = connect()
    cursor = con.cursor()
    cursor.execute("select count(*) from data;")
    count = cursor.fetchone()
    con.close()
    return count[0]


def picCount():
    con = connect()
    cursor = con.cursor()
    cursor.execute("select count(*) from picture;")
    count = cursor.fetchone()
    con.close()
    return count[0]

#############################################
################### PHONE ###################
#############################################

#CREATE TABLE bs(time int, long real, rat real, sender char(255), reciver char(255), Type char(255));

def bsQuery(rowData):
    if 'position' not in rowData.keys():
        return False
    if len(rowData['position']) == 4 or len(rowData['position']) == 0:
        return False
    time = util.timeTotimestamp(rowData['time'])
    lat, lon = util.locToCoord(rowData['position'])
    if 'sender' not in rowData:
        rowData['sender'] = 'None'
    if 'receiver' not in rowData:
        rowData['receiver'] = 'None'

    return time, lat, lon, rowData['sender'], rowData['receiver'], rowData['position'], rowData['type']


def input_django(datas) :
    level = 1
    id = 0
    for data in datas :
        if len(statics.objects.filter(pid = id, level = level, name = data)) != 0 :
            res       = statics.objects.get(pid = id, level = level, name = data)
            res.count = res.count + 1
            res.save()
            id        = res.id
            level     = level + 1
        else :
            dp    = statics(name = data, pid = id, count = 1, level = level)
            dp.save()
            id    = dp.id
            level = level + 1

def input(a, b) :
    loc   = util.toLoc(a, b)
    if loc == False :
        return False
    level = util.cutting(loc)
    input_django(level)

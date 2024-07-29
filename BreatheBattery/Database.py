#Contains all functions that deal with creating, closing, and inserting database records
import sqlite3
import sys

con = sqlite3.connect("BreatheBatteryPersistency.db")
cur = con.cursor()

def createDatabase():
    try:
        cur.execute("""CREATE TABLE PMDATA(time TEXT, SiteAddr TEXT, SiteName TEXT, app TEXT, area TEXT, date TEXT, 
        device_id TEXT, gps_alt REAL, gps_fix REAL, gps_lat REAL, gps_lon REAL, gps_num REAL, name TEXT, s_d0 REAL, 
        s_d1 REAL, s_d2 REAL, s_h0 REAL, s_t0 REAL, timestamp TEXT, CONSTRAINT unq UNIQUE (time, date, device_id))""")
        
        cur.execute("""CREATE TABLE DangerPeriods(Device_ID TEXT, BeginDate TEXT, BeginTime TEXT, EndDate TEXT, 
        EndTime TEXT, Periods INTEGER)""")
        
        cur.execute("""CREATE TABLE PollutionReport(Device_ID TEXT, Date TEXT, maxPollution REAL, minPollution REAL, 
        avgPollution REAL, CONSTRAINT unq UNIQUE (Device_ID, Date))""")
        
        con.commit()
        
    except sqlite3.OperationalError as e:
        print("No table created, all already pre-existed")
    except:
        e = sys.exc_info()[0]
        print("Unknown Error creating the database:",e)
    else:
        print("Databases BreatheBatteryPersistency, DangerPeriods, and PollutionReport created successfully")

def registerDangerPeriod(timeStamp,dangerDictionary,dangerPeriodCounter):
    dataList = [timeStamp["device_id"],dangerDictionary["BeginDate"],dangerDictionary["BeginTime"],
    timeStamp["date"],timeStamp["time"],dangerPeriodCounter]
    dangerPerData = ', '.join(["'"+str(item)+"'" for item in dataList])
    
    sql = f'INSERT INTO DangerPeriods(Device_ID, BeginDate, BeginTime, EndDate, EndTime, Periods) VALUES ({dangerPerData})'
    cur.execute(sql)

def insertPMdata(recordDictionary):

    cols_comma_separated = ', '.join(recordDictionary.keys())
    binds_comma_separated = ', '.join(["'"+str(item)+"'" for item in recordDictionary.values()])

    sql = f'INSERT OR IGNORE INTO PMDATA({cols_comma_separated}) VALUES ({binds_comma_separated})'

    try:
        cur.execute(sql)
    except sqlite3.OperationalError as e:
        print(f"Record of Device ID {recordDictionary['device_id']} cannot be parsed, since it contains an unknown column")

def closeConnection():
    con.commit()
    cur.close()
    con.close()
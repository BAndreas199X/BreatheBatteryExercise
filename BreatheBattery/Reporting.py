#contains all functions required for producing the reports
import Database
from datetime import datetime
import csv

def insertIntoPollutionReport(record):
    values = ', '.join(["'"+str(item)+"'" for item in record])
    sql = f"""INSERT OR IGNORE INTO PollutionReport(Device_ID, Date, maxPollution, 
    minPollution, avgPollution) VALUES ({values})"""
    Database.cur.execute(sql)

def deviceAnalysis(deviceID):
    sql = f"""SELECT device_id, date, MAX(s_d0), MIN(s_d0), ROUND(AVG(s_d0),2) FROM PMDATA WHERE device_id = '{deviceID}' 
    GROUP BY date"""
    
    Database.cur.execute(sql)
    resultExtremes = Database.cur.fetchall()
    
    for entry in resultExtremes:
        insertIntoPollutionReport(entry)

def exportDangerReport(timestamp):
    res = Database.cur.execute("SELECT * FROM DangerPeriods")
    rows = res.fetchall()
    
    if len(rows) == 0:
        print("No Danger Period Report created. No Danger Periods available!")
    else:
        with open(f'Danger_Period_Report_{timestamp}.csv', 'w', newline='') as csvfile:
            fieldnames = ["Device ID", "Begin Date", "Begin Time", "End Date", "End Time", "Periods Spanned"]
            writer = csv.writer(csvfile)
            writer.writerow(fieldnames)
            writer.writerows(rows) 

def exportPollutionReport(timestamp):
    res = Database.cur.execute("SELECT * FROM PollutionReport")
    rows = res.fetchall()

    with open(f'Pollution_Report_{timestamp}.csv', 'w', newline='') as csvfile:
        fieldnames = ["Device_ID", "Date", "Maximum Pollution", "Minimum Pollution","Average Pollution"]
        writer = csv.writer(csvfile)
        writer.writerow(fieldnames)
        writer.writerows(rows) 

def createReport():
    res = Database.cur.execute("SELECT DISTINCT device_id FROM PMDATA")
    deviceList = Database.cur.fetchall()
    
    for device in deviceList:
        deviceAnalysis(device[0])

    timestamp = datetime.now().strftime("%m-%d-%Y_%H-%M-%S")

    exportPollutionReport(timestamp)
    exportDangerReport(timestamp)
#Contains all functions repnsible for fetching and analyzing data
import Database
import requests
import json

def getJsonResponse(url):
    response_API = requests.get(url)
    try:
        response_API = requests.get(url)
        return response_API.json()
    except requests.exceptions.RequestException as e:
        print("Error accessing url: ",url,"RequestException",e)

def getListOfDeviceIDs():
    result = getJsonResponse("https://pm25.lass-net.org/API-1.0.0/project/airbox/latest/")
    device_ids = {feed["device_id"] for feed in result.get("feeds", [])}
    return list(device_ids)

def getOnlyKey(i_list):
    keys = list(i_list.keys())
    return str(keys[0])

def beginDangerPeriod(timeStamp):
    dangerDictionary = dict()
    dangerDictionary["BeginDate"] = timeStamp["date"]
    dangerDictionary["BeginTime"] = timeStamp["time"]
    return dangerDictionary

def iterateFeeds(i_feeds):

    isDangerPeriod = False
    activeDangerPeriod = dict()
    dangerPeriodCounter = 0
    
    currRecord = i_feeds[0]
    projectName = getOnlyKey(currRecord)
    resultTimeStamps = currRecord[projectName]
    
    for timeStamp in resultTimeStamps:
        currTimeStamp = getOnlyKey(timeStamp)
        
        timeStampInstance = timeStamp[currTimeStamp]
        
        Database.insertPMdata(timeStampInstance)
        
        if isDangerPeriod == False and timeStampInstance["s_d0"] >= 30:
        
            activeDangerPeriod = beginDangerPeriod(timeStampInstance)
            isDangerPeriod = True
            dangerPeriodCounter += 1
        elif isDangerPeriod == True and timeStampInstance["s_d0"] < 30:
        
            Database.registerDangerPeriod(timeStampInstance,activeDangerPeriod,dangerPeriodCounter)
            isDangerPeriod = False
            activeDangerPeriod = None
            dangerPeriodCounter = 0
        elif isDangerPeriod == True:
        
            dangerPeriodCounter += 1
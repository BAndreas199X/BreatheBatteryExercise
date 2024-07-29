import Reporting
import Database
import Dataparsing

print("Application initialized")

Database.createDatabase()

#get a list of all active Device-IDs
device_ids = Dataparsing.getListOfDeviceIDs()

"""this loop will iterate until it finds a device that produced records
as soon as the first device producing records has been found an analyzed, the application will break
This way it should be guaranteed that exactely one recording producing device is analyzed
If ALL active devices should be evaluated, the final "If"-clause can be removed"""
for deviceID in device_ids:
    records = Dataparsing.getJsonResponse("https://pm25.lass-net.org/API-1.0.0/device/"+deviceID+"/history/?format=JSON")
    
    if records is None or records["num_of_records"] == 0:
        continue;
    
    feeds = records["feeds"]
    
    Dataparsing.iterateFeeds(feeds)
    
    if records["num_of_records"] != 0:
        break;
        
Reporting.createReport()

Database.closeConnection()

print("Application has concluded")

  
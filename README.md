BreatheBattery.py is the main file
Reporting.py contains all functions required for producing the reports
Dataparsing.py contains all functions repnsible for fetching and analyzing data
Reports.py contains all functions required for producing the reports

The application is written to parse the data for one device/one device-ID at a time. 
This is because the API is slow, but also because the instructions state to "read the data for *a* (singular) device".
If ALL active devices should be evaluated, the final "If"-clause in the main-program can be removed.

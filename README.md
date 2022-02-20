# Data Engineer Internship Task

This project audits and cleans raw turbine data then load them to the database (mongodb). This project also includes django to serve data to the user through data dashboard. The data is saved under directory data/raw/.  

This project composed of 2 part:
 - data process (use python script and mongodb)
 - data display (django)

## Deploy locally with Docker Compose

Docker Compose script provides production-ready stack consisting of the following components:
 - MongoDB
 - Django-Gunicorn
 - Nginx

create .env file:
```bash
cp .env.example .env
```
then edit creadentials inside .env file

To start using the app from http://localhost:8000 run this command:
```bash
docker-compose -f docker-compose.yml build
docker-compose -f docker-compose.yml up -d
```
Check on the http://localhost:8000 you will see 2 graph with no data because we have not load the data yet.

## Data Process (Audit, Clean, Load)

 - install required package:
```bash
pip install -r requirement.txt
```

 - audit the data:
```bash
python script/audit.py -f <path to the raw data>

python script/audit.py -f data/raw/Turbine1.csv
```
There are 2 audits done by this script, the first one is to check wether all of the column contain numerical or non-numerical value. The second one is to check null value among data point. Repeat this process for Turbine2.csv

 - then clean the data using: 
```bash
python script/clean.py -f <path to the raw data file> -o <path to the clean data folder>

python script/clean.py -f data/raw/Turbine1.csv -o data/clean/ 

```
this process move the first row of the raw data which contain measurement units to the new column. . Repeat this process for Turbine2.csv. Make sure after clean all of the data to run the audit script to the clean data csv file to check the data quality.

 - after that load the data to db using: 
```bash
python script/load.py -f <path to the clean data file> -u <db username> -p <db password> -a <db host> -d <database name> -c <collection name>

python script/load.py -f data/clean/Turbine1.csv -u <db username> -p <db password> -a localhost:27017 -d development -c turbine-1
```
repeat this process for Turbine2 clean data, dont forget to change the collection name when loading the Turbine2 data. Check on the http://localhost:8000 and choose date range, data type to be displayed.

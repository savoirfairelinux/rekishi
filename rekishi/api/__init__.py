from influxdb import client as influxdb
from utils.influxdb_model import *

from rekishi import settings

host = settings.INFLUXDB_HOST
print "***********", host, "************"
port = settings.INFLUXDB_PORT
username = settings.INFLUXDB_USER
password = settings.INFLUXDB_PASSWORD
database = settings.INFLUXDB_DB

db = influxdb.InfluxDBClient(host, port, username, password, database)

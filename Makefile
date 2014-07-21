build-influxdb:
	docker build -t ppepos/influxdb containers/influxdb
run-influxdb:
	docker run -p 8083:8083 -p 8084:8084 -p 8086:8086 -i -t influxdb /bin/bash

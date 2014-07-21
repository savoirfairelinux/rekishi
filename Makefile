build-shinken:
	cp containers/shinken/scripts/tokens.py.copyme containers/shinken/scripts/tokens.py
	cd containers/shinken && make conf
	sudo docker build -t shinken containers/shinken

build-influxdb:
	sudo docker build -t influxdb containers/influxdb

run-shinken:
	sudo docker run -d -t shinken
	
run-influxdb:
	sudo docker run -d -t influxdb
	# docker run -p 8083:8083 -p 8084:8084 -p 8086:8086 -i -t influxdb /bin/bash

build-shinken:
	cp containers/shinken/scripts/tokens.py.copyme containers/shinken/scripts/tokens.py
	cd containers/shinken && make conf
	docker build -t shinken containers/shinken

build-influxdb:
	docker build -t influxdb containers/influxdb

run-influxdb:
	docker run -p 8083:8083 -p 8084:8084 -p 8086:8086 -i -t influxdb /bin/bash

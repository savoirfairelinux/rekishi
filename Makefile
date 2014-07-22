build-shinken:
	pip install beautifulsoup4
	pip install requests
	cp containers/shinken/scripts/tokens.py.copyme containers/shinken/scripts/tokens.py
	cd containers/shinken && make conf
	docker.io build  -t quebecmon containers/shinken

build-influxdb:
	docker.io build -t influxdb containers/influxdb
	# docker.io build --no-cache=true -t influxdb containers/influxdb

run-shinken:
	# docker.io rm shinken
	docker.io run -i -t --name shinken --link db:db quebecmon bash
	
run-influxdb:
	# docker.io run -i -t -P influxdb
	docker.io rm db
	docker.io run -d -t -p 8083:8083 -p 8086:8086 --name db influxdb
	# docker.io run -p 8083:8083 -p 8084:8084 -p 8086:8086 -i -t influxdb /bin/bash

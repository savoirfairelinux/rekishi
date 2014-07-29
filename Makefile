all: clean build-shinken build-influxdb run-influxdb run-shinken 

build-all: build-shinken build-influxdb

run-all: run-shinken run-influxdb

clean:
	docker stop shinken
	docker stop db
	docker rm shinken
	docker rm db

build-shinken:
	pip install beautifulsoup4
	pip install requests
	cp containers/shinken/scripts/tokens.py.copyme containers/shinken/scripts/tokens.py
	cd containers/shinken && make conf
	docker build -t quebecmon containers/shinken

build-influxdb:
	docker build -t influxdb containers/influxdb

run-shinken:
	docker run -d -t --name shinken --link db:db quebecmon
	
run-influxdb:
	docker run -d -v ${PWD}/containers/data:/data/db -t -p 8083:8083 -p 8086:8086 --name db influxdb

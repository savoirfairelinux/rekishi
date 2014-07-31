all: clean build-shinken build-influxdb run-influxdb run-shinken 

build-all: build-shinken build-influxdb

run-all: run-influxdb run-shinken

clean:
	true

kill:
	sudo docker stop shinken
	sudo docker stop db
	sudo docker rm shinken
	sudo docker rm db

build-shinken:
	cd containers/shinken && make conf
	sudo docker build -t quebecmon containers/shinken

build-influxdb:
	sudo docker build -t influxdb containers/influxdb

run-shinken:
	sudo docker run -d -t --name shinken --link db:db quebecmon

run-influxdb:
	sudo docker run -d -v ${PWD}/containers/data:/data -t -p 8083:8083 -p 8086:8086 --name db influxdb

all: clean build-shinken build-influxdb build-rekishi build-apache run-influxdb run-rekishi run-shinken run-apache

build-all: build-shinken build-influxdb build-rekishi build-apache

run-all: run-influxdb run-rekishi run-shinken run-apache

clean:
	true

kill:
	sudo docker stop shinken
	sudo docker stop db
	sudo docker stop rekishi
	sudo docker stop apache
	sudo docker rm shinken
	sudo docker rm db
	sudo docker rm rekishi
	sudo docker rm apache

build-shinken:
	cd containers/shinken && make conf
	sudo docker build -t quebecmon containers/shinken

build-influxdb:
	sudo docker build -t influxdb containers/influxdb

build-rekishi:
	sudo docker build -t rekishi containers/rekishi

build-apache:
	sudo docker build -t apache containers/apache

run-shinken:
	@if [ -z "$(ADAGIOS_PATH)" ]; then \
		sudo docker run -d -t --name shinken --link db:db quebecmon; \
		echo "sudo docker run -d -t --name shinken --link db:db quebecmon"; \
	else \
	sudo docker run -i -t --name shinken --link db:db -p 8002:8000 --volume=$(ADAGIOS_PATH):/opt/adagios quebecmon bash; \
		echo "sudo docker run -d -t --name shinken --link db:db --volume=$(ADAGIOS_PATH):/opt/adagios quebecmon"; \
	fi

run-influxdb:
	sudo docker run -d -v ${PWD}/containers/data:/data -t -p 8083:8083 -p 8086:8086 --name db influxdb

run-rekishi:
	sudo docker run -d -v ${PWD}:/opt/rekishi -t -p 8001:8000 --name rekishi --link db:db rekishi

run-apache:
	sudo docker run -d -t -p 80:80 --name apache apache


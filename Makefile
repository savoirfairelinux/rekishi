all: clean build-shinken build-influxdb build-rekishi run-influxdb run-shinken run-rekishi

build-all: build-shinken build-influxdb build-rekishi

run-all: run-influxdb run-shinken run-rekishi

clean:
	true

kill:
	sudo docker stop shinken
	sudo docker stop db
	sudo docker stop rekishi
	sudo docker rm shinken
	sudo docker rm db
	sudo docker rm rekishi

build-shinken:
	cd containers/shinken && make conf
	sudo docker build -t quebecmon containers/shinken

build-influxdb:
	sudo docker build -t influxdb containers/influxdb

build-rekishi:
	sudo docker build -t rekishi containers/rekishi

run-shinken:
	@if [ -z "$(ADAGIOS_PATH)" ]; then \
		sudo docker run -d -t --name shinken --link db:db quebecmon; \
		echo "sudo docker run -d -t --name shinken --link db:db quebecmon"; \
	else \
	sudo docker run -d -t --name shinken --link db:db -p 8000:8000 --volume=$(ADAGIOS_PATH):/opt/adagios quebecmon; \
		echo "sudo docker run -d -t --name shinken --link db:db --volume=$(ADAGIOS_PATH):/opt/adagios quebecmon"; \
	fi

run-influxdb:
	sudo docker run -d -v ${PWD}/containers/data:/data -t -p 8083:8083 -p 8086:8086 --name db influxdb

run-rekishi:
	sudo docker run -d -v ${PWD}:/opt/rekishi -t -p 8000:8001 --name rekishi --link db:db rekishi

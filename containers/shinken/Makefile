all: conf run

run:
	docker.io build -t quebec .
	docker.io run -d -p 8080:80 quebec

conf: banks transports environment

banks:
	# scripts/banks.py > etc/shinken/adagios/banks.cfg

transports:
	scripts/transports.py > etc/shinken/adagios/transports.cfg

environment:
	scripts/environment.py > etc/shinken/adagios/environment.cfg

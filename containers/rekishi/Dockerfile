FROM ubuntu:trusty

MAINTAINER Matthieu Caneill <matthieu.caneill@savoirfairelinux.com>
MAINTAINER Philippe Pepos Petitclerc <philippe.pepos-petitclerc@savoirfairelinux.com>

ENV DEBIAN_FRONTEND noninteractive

### Init

RUN apt-get update

### Utils

RUN apt-get install -y git python-pip emacs curl vim

### SSH
RUN apt-get install -y openssh-server
ADD id_rsa.pub /root/.ssh/authorized_keys

### Supervisor
RUN apt-get -y install supervisor

### Django
RUN pip install django\<1.7
RUN pip install influxdb
RUN ln -s /usr/bin/django-admin /usr/bin/django-admin.py

### Copy configs
ADD etc /etc

### SSH and Django
EXPOSE 22
EXPOSE 8000

ENV INFLUXDB_HOST db

CMD ["/usr/bin/supervisord"]

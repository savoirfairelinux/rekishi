FROM ubuntu:trusty

MAINTAINER Matthieu Caneill <matthieu.caneill@savoirfairelinux.com>
MAINTAINER Philippe Pepos Petitclerc <philippe.pepos-petitclerc@savoirfairelinux.com>

ENV DEBIAN_FRONTEND noninteractive

### Init

RUN apt-get update

### Utils

RUN apt-get install -y git python-pip emacs curl vim

### Other .deb sources

RUN curl http://download.opensuse.org/repositories/home:/sfl-monitoring:/monitoring-tools/xUbuntu_14.04/Release.key | apt-key add -
RUN echo 'deb http://download.opensuse.org/repositories/home:/sfl-monitoring:/monitoring-tools/xUbuntu_14.04/ /' >> /etc/apt/sources.list.d/shinkenplugins.list

RUN apt-get update

### Shinken

RUN useradd shinken
RUN pip install https://github.com/naparuba/shinken/archive/master.tar.gz

RUN apt-get install -y python-openssl # required for $plugin
RUN apt-get install -y python-lxml # required by scrapers plugins
RUN apt-get install -y python-protobuf # required by check_amt


### SSH

run apt-get install -y openssh-server

### Supervisor

RUN apt-get -y install supervisor

### Configuration

## Shinken

RUN apt-get install -y python-pycurl
RUN pip install influxdb
RUN shinken --init
RUN shinken install mod-influxdb
RUN shinken install graphite
RUN shinken install livestatus
RUN shinken install pickle-retention-file-generic
RUN shinken install simple-log
RUN shinken install booster-nrpe
RUN shinken install logstore-sqlite
RUN rm /etc/shinken/modules/influxdb.cfg
RUN rm /etc/shinken/brokers/broker-master.cfg

### Plugins

RUN apt-get install -y nagios-plugins
RUN apt-get install -y plugin-check-amt-montreal plugin-check-bixi-montreal plugin-check-environment-canada plugin-check-http2 plugin-check-stm-metro-montreal

# TODO: change Shinken conf for that
RUN cp /usr/lib/shinken/plugins/* /var/lib/shinken/libexec/

# run permissions for user `shinken`
RUN chmod u+s /usr/lib/nagios/plugins/check_icmp
RUN chmod u+s /bin/ping
RUN chmod u+s /bin/ping6

ADD etc /etc
RUN chown -R shinken: /etc/shinken

EXPOSE 22

CMD ["/usr/bin/supervisord"]

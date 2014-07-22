FROM ubuntu:trusty

MAINTAINER Matthieu Caneill <matthieu.caneill@savoirfairelinux.com>
CONTRIBUTOR Philippe Pepos Petitclerc <philippe.pepos-petitclerc@savoirfairelinux.com>

ENV DEBIAN_FRONTEND noninteractive

### Init

RUN apt-get update

### Utils

RUN apt-get install -y git python-pip emacs curl vim

### Other .deb sources

RUN curl http://download.opensuse.org/repositories/home:/kaji-project/xUbuntu_14.04/Release.key | apt-key add -
RUN echo 'deb http://download.opensuse.org/repositories/home:/kaji-project/xUbuntu_14.04/ /' >> /etc/apt/sources.list.d/kaji.list

RUN curl http://download.opensuse.org/repositories/home:/ReAzem:/sfl-shinken-plugins/xUbuntu_14.04/Release.key | apt-key add -
RUN echo 'deb http://download.opensuse.org/repositories/home:/ReAzem:/sfl-shinken-plugins/xUbuntu_14.04/ /' >> /etc/apt/sources.list.d/shinkenplugins.list

RUN apt-get update

### Shinken

RUN useradd shinken
RUN pip install https://github.com/naparuba/shinken/archive/master.tar.gz

# Temp removal because mod-influxdb requires shinken-latest
# RUN apt-get install -y shinken-common
# RUN apt-get install -y shinken-module-graphite
# RUN apt-get install -y shinken-module-livestatus
# RUN apt-get install -y shinken-module-pickle-retention-file-generic
# RUN apt-get install -y shinken-module-simple-log
# RUN apt-get install -y shinken-module-booster-nrpe
# RUN apt-get install -y shinken-module-logstore-sqlite

RUN apt-get install -y python-openssl # required for $plugin
RUN apt-get install -y python-lxml # required by scrapers plugins
RUN apt-get install -y python-protobuf # required by check_amt


### SSH

RUN apt-get install -y openssh-server

### Supervisor

RUN apt-get -y install supervisor

### Configuration

## Shinken

# RUN mv /etc/shinken/logstore_sqlite.cfg/logstore_sqlite.cfg /etc/shinken/modules/
# RUN sed -i 's/logstore-sqlite/logsqlite/g' /etc/shinken/modules/logstore_sqlite.cfg
# RUN sed -i 's/Livestatus/livestatus/g' /etc/shinken/brokers/broker.cfg
# RUN sed -i 's/Simple-log/simple-log/g' /etc/shinken/brokers/broker.cfg
# RUN sed -i 's/NrpeBooster/booster-nrpe/g' /etc/shinken/pollers/poller.cfg

# Allow ssh connection from host
ADD id_rsa.pub /root/home/.ssh/authorized_keys

# mod-influxdb
# RUN mkdir -p /var/lib/shinken/cli
# RUN mkdir -p /var/lib/shinken/modules
# RUN mkdir -p /var/lib/shinken/share
# RUN mkdir -p /var/lib/shinken/doc
# RUN mkdir -p /var/lib/shinken/inventory
# ADD cli /var/lib/shinken/cli

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

# temporary fix while we wait for https://github.com/shinken-monitoring/mod-livestatus/pull/26
ADD mod-livestatus-labels.patch /mod-livestatus-labels.patch
# RUN cd /var/lib/shinken/modules/livestatus && git apply /mod-livestatus-labels.patch

### Plugins

RUN apt-get install -y nagios-plugins
RUN apt-get update -v
RUN apt-get update
#delete me
RUN apt-get install -y plugin-check-amt-montreal plugin-check-bixi-montreal plugin-check-emergency-rooms-quebec plugin-check-environment-canada plugin-check-http2 plugin-check-quebecrencontrescom plugin-check-reseaucontactcom plugin-check-stm-metro-montreal
RUN cp /usr/lib/shinken/plugins/* /var/lib/shinken/libexec/

## Docker

# makes `df` work
# RUN ln -s /proc/mounts /etc/mtab

# run permissions for user `shinken`
RUN chmod u+s /usr/lib/nagios/plugins/check_icmp
RUN chmod u+s /bin/ping
RUN chmod u+s /bin/ping6

ADD etc /etc
RUN chown -R shinken: /etc/shinken
RUN sed -i 's/HOSTTOREPLACE/'"$DB_PORT_8086_TCP_ADDR"'/gi' /etc/shinken/modules/influxdb.cfg

EXPOSE 22

CMD ["/usr/bin/supervisord"]

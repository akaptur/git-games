FROM ubuntu:latest
MAINTAINER Allison Kaptur <allison.kaptur@gmail.com>
RUN DEBIAN_FRONTEND=noninteractive apt-get -y install git
EXPOSE 80
EXPOSE 22
CMD ["/bin/bash", "/start.sh"]

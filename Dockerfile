ARG DATA_DIR=/opt/data
FROM centos:8 as centos-py36-nginx

RUN yum -y update &&\
    dnf -y update &&\
    dnf -y install dnf-utils &&\
    yum clean all && dnf clean all

ADD etc/yum.repos.d/nginx.repo /etc/yum.repos.d/nginx.repo

#should come from regularly rotated, trusted (internal store over private subnets) keystore in production
RUN rpm --import  https://nginx.org/keys/nginx_signing.key &&\
    yum-config-manager --enable nginx-mainline &&\
    dnf -y install nginx python3 python3-pip &&\
    # I checked first there was no /usr/bin/python|pip yet and python|pip was not installed anywhere else
    ln -f /usr/bin/python3 /usr/bin/python &&\
    ln -f /usr/bin/pip3 /usr/bin/pip &&\
    rm -rf /etc/nginx/conf.d &&\
    dnf clean all

ADD etc/nginx /etc/nginx

FROM centos-py36-nginx as server-build

RUN useradd asgi-user 

WORKDIR /home/asgi-user

USER asgi-user

ENV DATA_DIR=$DATA_DIR

ADD src/python apps

USER root

WORKDIR /home/asgi-user/apps/imdb_analyzer

RUN pip install -r server-requirements.txt

ENV DATA_DIR=$DATA_DIR

RUN chmod 0750 server/server-controller.sh 

EXPOSE 80

ENTRYPOINT ["server/server-controller.sh","start"]
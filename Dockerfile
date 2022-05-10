
# I know it doesn't save me any space but it doesn't cost any and I like the organization
# I have an old version of docker on this laptop that has an issue with 'blank string override'
# ARG OPT_DIR=/opt/ml-analyzer
FROM centos as centos-py36-nginx

ENV OPT_DIR=/opt/ml-analyzer
ENV DATA_DIR=$OPT_DIR/data
ENV DATA_FILE=movie_metadata.csv

RUN mkdir -p $DATA_DIR &&\
    yum -y update &&\
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

ADD server-requirements.txt $OPT_DIR

RUN pip install --no-cache -r $OPT_DIR/server-requirements.txt &&\
    useradd asgi-user 

WORKDIR /home/asgi-user

USER asgi-user

ADD src/python apps

USER root

WORKDIR /home/asgi-user/apps/imdb_analyzer

RUN chmod 0750 server/server-controller.sh &&\
    chown -R asgi-user:nginx $DATA_DIR

EXPOSE 80

ENTRYPOINT ["server/server-controller.sh","start"]
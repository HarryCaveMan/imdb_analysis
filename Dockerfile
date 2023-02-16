
# I know it doesn't save me any space but it doesn't cost any and I like the organization
# I have an old version of docker on this laptop that has an issue with 'blank string override'
# ARG OPT_DIR=/opt/ml-analyzer
FROM amazonlinux:2 as centos-py36-nginx

ENV OPT_DIR=/opt/ml-analyzer
ENV DATA_DIR=$OPT_DIR/data
ENV DATA_FILE=movie_metadata.csv

RUN mkdir -p $DATA_DIR &&\
    amazon-linux-extras enable nginx1 python3.8 &&\
    yum -y clean metadata && yum -y update &&\
    yum -y install shadow-utils acl nginx python3.8 &&\
    ln -f /usr/bin/python3.8 /usr/bin/python3 && ln -f /usr/bin/pip3.8 /usr/bin/pip3 &&\
    # dnf -y update &&\
    # dnf -y install dnf-utils &&\
    yum clean all && rm -rf /var/cache/yum

ADD etc/nginx /etc/nginx

ADD server-requirements.txt $OPT_DIR

RUN pip3 install --no-cache -r $OPT_DIR/server-requirements.txt &&\
    useradd asgi-user 

WORKDIR /home/asgi-user

USER asgi-user

ADD src/python apps

USER root

WORKDIR /home/asgi-user/apps/imdb_analyzer

RUN chmod 0750 server/server-controller.sh &&\
    chown -R asgi-user:asgi-user $DATA_DIR

EXPOSE 80

ENTRYPOINT ["server/server-controller.sh","start"]
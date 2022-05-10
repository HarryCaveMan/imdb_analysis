#!/bin/bash

start(){
    if [ `whoami`='root' ]; then
       nginx
       setfacl -m u:asgi-user:rwx /tmp
       PYTHONPATH=.
       gunicorn \
         -u asgi-user \
         -g nginx \
         -b unix:/tmp/gunicorn.sock \
         -m 007 \
         -w 4 -k uvicorn.workers.UvicornH11Worker \
         server:app
    else
        echo "must be root!"
        exit 1
    fi
}

stop() {
    if [ `whoami`='root' ]; then
       nginx -s stop
       pkill gunicorn
    else
        echo "must be root!"
        exit 1
    fi
}

restart() {
  stop
  #TODO wait should poll that port 80 is unbound (maybe on 1sec interval) and sockfile is cleaned up
  sleep 15
  start
}


case $1 in
  start|stop|restart)
    $1
  ;;
  *)
    echo "unsuported arg (start|stop|restart suported)"
    exit 1
  ;;
esac
    
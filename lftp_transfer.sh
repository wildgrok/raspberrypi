#!/bin/bash

HOST=besada.com
USER=jbesada
PASSWORD=Camello2183
LOCALPATH=/var/www/html/coronavirus/state_deaths
FILE=*.*
REMOTEPATH=/public_html/coronavirus/state_deaths/


ftp -n -v $HOST <<EOT

binary
user $USER $PASSWORD
prompt
lcd $LOCALPATH
cd $REMOTEPATH

mput $FILE

lcd /var/www/html/coronavirus
cd /public_html/coronavirus/
mput *.html



bye
EOT

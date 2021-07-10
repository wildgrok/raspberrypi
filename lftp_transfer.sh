#!/bin/bash

HOST=besada.com
USER=jbesada
PASSWORD=Camello2183
LOCALPATH=/home/pi/Documents/
FILE=*.csv
REMOTEPATH=/public_html


ftp -n -v $HOST <<EOT

binary
user $USER $PASSWORD
prompt
lcd $LOCALPATH
cd $REMOTEPATH

mput $FILE
bye
EOT

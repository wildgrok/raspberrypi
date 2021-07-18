#!/bin/bash

HOST=besada.com
USER=jbesada
PASSWORD=Camello2183
LOCALPATH=//var/www/html/coronavirus/
FILE=references2.html
REMOTEPATH=/public_html/coronavirus


ftp -n -v $HOST <<EOT

binary
user $USER $PASSWORD
prompt
lcd $LOCALPATH
cd $REMOTEPATH

get $FILE
bye
EOT

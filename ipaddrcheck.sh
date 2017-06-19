#!/bin/bash
curl -o ~/newip ifconfig.co
cmp ~/newip ~/oldip >/dev/null || {
mv ~/newip ~/oldip 
mailx -r jbesad@gmail.com -s "I - IP ${HOSTNAME} changed" jbesad@yahoo.com < ~/oldip
} 

#!/bin/bash

# go to home
cd ~

# open firefox in main website
firefox http://company.pt &

# retry client app while server is down
while true
do
	# open client with supressed error output
	sudo python3 client.py 2>/dev/null

	if [ $? == 0 ]
	then
		break
	else
		echo "Server is down."
		echo "Retrying..."
	fi

	sleep 1

	clear
done

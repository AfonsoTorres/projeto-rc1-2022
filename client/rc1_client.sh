#!/bin/bash

# go to home
cd ~

# open firefox in main website
firefox http://sungla.pt &

# retry client app while server is down
while true
do
	# open client with supressed error output
	python3 client.py

	if [ $? == 0 ]
	then
		break
	else
		clear
		echo "Server is down."
		echo "Retrying..."
	fi

	sleep 1

	clear
done

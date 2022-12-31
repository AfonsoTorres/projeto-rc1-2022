#!/bin/bash

# go to home
cd ~

# open server
while true
do
	sudo python3 server.py

	if [ $? == 0 ]
	then
		break
	else
		clear
		echo "Port in use."
		echo "Retrying..."
	fi

	sleep 1
	
	clear
done

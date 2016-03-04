#!/bin/sh

HAR_DIR=~/harstorage/harfiles
HS_URL="http://localhost:5000"

for i in `ls $HAR_DIR/*.har`  
do  
	echo "Uploading $i"  
	curl -s -X POST --form "file=@$i" --header "Automated: true" $HS_URL/results/upload
done  

# Example
#curl -X POST --form "file=@~/harstorage/harfiles/www.stubhub.com--origin-wro-2013-02-01-13-08-06.har" --header "Automated: true" $HS_URL/results/upload



#!/bin/bash

manual_data_points=10
automated_data_points=9
company_count=$(cat pdfcount.txt | wc -l)

automation_time=$((5*60))
manual_time=5

# >30 is where automation will start to become useful
manual_companies=$(cat pdfcount.txt  | awk '$1 < 30 {print}' | wc -l)
auto_companies=$(cat pdfcount.txt  | awk '$1 > 30 {print}' | wc -l)
mcpc=$(cat pdfcount.txt  | awk '$1 < 30 {print $1 }' | st -s)
acpc=$(cat pdfcount.txt  | awk '$1 > 30 {print $1 }' | st -s)

echo automation time: $(($auto_companies*$automated_data_points*$automation_time/3600)) hours

echo manual time: $(( ( $mcpc*$manual_companies*($manual_data_points+$automated_data_points) +\
	($acpc*$auto_companies*$manual_time))/ 3600 )) hours

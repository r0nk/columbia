#!/bin/bash

#remove spaces
#find | while read i; do mv "$i" `echo $i | tr ' ' '_'`; done

#get text versions of all the pdfs
#for i in $(ls | grep pdf) ; do pdftotext -layout $i ; done

#counts of all pdfs
#find | grep -E "\.pdf$" | tr '\/' ' '  | awk '{print $2}' | sus > pdfcount.txt

#no Registro, appears to mean ICA registro number

#the output of this file should ultimately be a csv

#so for every given file, output csv entries

#so the general idea is to do entries for everything, then figure out what isn't being enetered somewhere and going there and fixing it.

pdf_to_csv(){
	filename=$1
	tmpfile=$(mktemp)
	pdftotext -layout $1 $tmpfile

	registration_number=$(cat $tmpfile | grep -i Registro | grep -i nacional | grep -o "[0-9]*")

	product_name=$(cat $tmpfile | grep -i "descrip" -A 1 | grep -v "DESCRIP" |  grep -Eo "^[^(a-z|,)]*")

	company_name=$(echo $filename | tr '\/' ' ' | awk '{print $1}')

	registration_holder=$( cat $tmpfile | grep -i registro | grep -i titular | sed "s/TITULAR DEL REGISTRO//g")

	active_ingredient=$( cat $tmpfile | grep -i "Ingrediente Activo:" | sed "s/Ingrediente Activo://g;")

	product_class=$(cat $tmpfile | grep -Eio "(insect|herb|fung)icida"| head -n 1)

	formulation_type=$( cat $tmpfile | grep -i "tipo de formulac" | sed "s/.*://g")

	printf "%s, " $filename
	printf "%s, " $registration_number
	printf "%s, " $product_name
	printf "%s, " $company_name
	printf "%s, " $registration_holder
	printf "%s, " $active_ingredient
	printf "%s, " $product_class
	printf "%s, " $formulation_type

	#these are all TODO
	printf "%s, " $crop
	printf "%s, " $pests
	printf "%s, " $application_type
	printf "%s, " $application_timing
	printf "%s, " $dose
	printf "%s, " $dose_units
	printf "%s, " $waiting_period
	printf "%s, " $reentry_interval
	printf "%s, " $number_of_applications
	printf "%s, " $application_interval
	printf "%s" $notes

	printf "\n"

	rm $tmpfile
}

#header
echo filename,registration_number,product_name,company_name,registration_holder,active_ingredient,product_class,formulation_type,crop,pests,application_type,application_timing,dose,dose_units,waiting_period,reentry_interval,number_of_applications,application_interval,notes

for i in $(find -type f | grep -E "pdf$" ) ; do pdf_to_csv $i ; done

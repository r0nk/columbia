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
	echo "converting $filename"
	tmpfile=$(mktemp)
	pdftotext -layout $1 $tmpfile

	registration_number=$(cat $tmpfile | grep -i Registro | grep -i nacional | grep -o "[0-9]*")
	echo registration_number: $registration_number

	product_name=$(cat $tmpfile | grep -i "descrip" -A 1 | grep -v "DESCRIP" |  grep -Eo "^[^(a-z|,)]*")
	echo "product_name: $product_name"

	company_name=$(echo $filename | tr '\/' ' ' | awk '{print $1}')
	echo "company_name: $company_name"

	registration_holder=$( cat $tmpfile | grep -i registro | grep -i titular | sed "s/TITULAR DEL REGISTRO//g")
	echo registration_holder: $registration_holder

	active_ingredient=$( cat $tmpfile | grep -i "Ingrediente Activo:" | sed "s/Ingrediente Activo://g;")
	echo active_ingredient: $active_ingredient

	product_class=$(cat $tmpfile | grep -Eio "(insect|herb|fung)icida"| head -n 1)
	echo product_class: $product_class

	formulation_type=$( cat $tmpfile | grep -i "tipo de formulac" | sed "s/.*://g")
	echo formulation_type: $formulation_type

	rm $tmpfile
}

pdf_to_csv UPL/Abamecal.pdf

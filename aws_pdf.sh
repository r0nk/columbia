#!/bin/bash
filename="$1"
out=$(echo $filename | sed "s/\//\-/g" | sed "s/pdf/json/g")
jobid=$(aws textract start-document-analysis --document-location "{\"S3Object\":{\"Bucket\":\"sst3i-columbia\",\"Name\":\"$filename\"}}" --feature-types '["TABLES","FORMS"]' | jq .JobId | sed "s/\"//g")
echo $out $jobid $(date -Im) starting... 
sleep 120
aws textract get-document-analysis --job-id $jobid > $out
echo $out $jobid $(date -Im) DONE 


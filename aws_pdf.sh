#!/bin/bash
bucket_name="asdf"
aws textract start-document-analysis --document-location '{"S3Object":{"Bucket":"$bucket_name","Name":"columbia/Agrocentro/BUTACLOR-600-EC.pdf"}}' --feature-types '["TABLES","FORMS"]' | jq .JobId > jobid.txt
aws textract get-document-analysis --job-id $(cat jobid.txt) > blockout.json


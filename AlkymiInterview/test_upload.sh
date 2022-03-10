#!/bin/bash
curl --location --request POST 'http://127.0.0.1:8000/v1/table?headerRow=true' \
--header 'Content-Disposition: attachment; filename=AlkymiTest.csv' \
--header 'Content-Type: application/octet-stream' \
--header "Authorization: Token $1" \
--data-binary "@`pwd`/../AlkymiTestFile.csv"

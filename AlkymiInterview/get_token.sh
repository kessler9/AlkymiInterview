#!/bin/bash
curl --location --request POST 'http://127.0.0.1:8000/api-token-auth/' \
--form "username=\"$1\"" \
--form "password=\"$2\""

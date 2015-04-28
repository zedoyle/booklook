#!/bin/bash
rm ./google_result.json
touch ./google_result.json
./googler.py &> /dev/null
cat ./google_result.json

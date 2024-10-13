#!/bin/bash

# Get the script directory
SCRIPT_DIR=$(cd $(dirname "$0") && pwd)

# Remove existing deployment package if it exists
if [ -f ${SCRIPT_DIR}/deployment_package.zip ]; then
  rm -f ${SCRIPT_DIR}/deployment_package.zip
fi

cd ${SCRIPT_DIR}/lambda
zip -r ${SCRIPT_DIR}/deployment_package.zip . >> /dev/null 2>&1


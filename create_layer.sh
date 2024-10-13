#!/bin/bash

# Get the script directory
SCRIPT_DIR=$(cd $(dirname "$0") && pwd)

# Remove existing deployment package if it exists
if [ -f ${SCRIPT_DIR}/layer_content.zip ]; then
  rm -f ${SCRIPT_DIR}/layer_content.zip
fi

mkdir ${SCRIPT_DIR}/python
cp -r ${SCRIPT_DIR}/.venv/lib ${SCRIPT_DIR}/python/

cd ${SCRIPT_DIR}
zip -r ${SCRIPT_DIR}/layer_content.zip ./python >> /dev/null 2>&1

rm -rf ${SCRIPT_DIR}/python

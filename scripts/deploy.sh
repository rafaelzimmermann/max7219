#!/bin/bash

SCRIPT_PATH=$(dirname "$0")
source "${SCRIPT_PATH}/base.sh"

mount_pico

echo "Deploy started"

rm -f "${MOUNT_POINT}/libs"
cp -r libs "${MOUNT_POINT}"
cp *.py "${MOUNT_POINT}"
cp *.bin "${MOUNT_POINT}"

echo "Deploy done"

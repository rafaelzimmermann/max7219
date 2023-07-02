#!/bin/bash

SCRIPT_PATH=$(dirname "$0")
source "${SCRIPT_PATH}/base.sh"

mount_pico

VERSION="8.1.0"

rm -f /mnt/pico/adafruit-circuitpython-raspberry_pi_pico-en_US-${VERSION}.uf2

wget \
    "https://downloads.circuitpython.org/bin/raspberry_pi_pico/en_US/adafruit-circuitpython-raspberry_pi_pico-en_US-${VERSION}.uf2" \
    -O "/tmp/adafruit-circuitpython-raspberry_pi_pico-en_US-${VERSION}.uf2"
mv "/tmp/adafruit-circuitpython-raspberry_pi_pico-en_US-${VERSION}.uf2" "/mnt/pico/adafruit-circuitpython-raspberry_pi_pico-en_US-${VERSION}.uf2"
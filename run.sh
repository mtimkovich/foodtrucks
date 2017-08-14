#!/bin/sh

cd $(dirname $0)
. env/bin/activate
./food_trucks.py

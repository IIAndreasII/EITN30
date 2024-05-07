#!/usr/bin/bash

route del default
ip route add default via 11.11.11.3 dev MyG

#!/usr/bin/bash

sudo ip route add 10.8.0.0/16 via 130.235.200.1
sudo ip route add default via 11.11.11.3 dev MyG

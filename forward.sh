#!/usr/bin/bash


iptables -t nat -A POSTROUTING -o eth0 -j MASQUERADE

iptables -A FORWARD -i eth0 -o MyG -m state --state RELATED,ESTABLISHED -j ACCEPT

iptables -A FORWARD -i MyG -o eth0 -j ACCEPT

iptables -A FORWARD -i eth0 -o MyG -m state --state RELATED,ESTABLISHED -m limit --limit 10/sec -j ACCEPT
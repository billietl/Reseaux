#!/bin/bash

# Regles iptables
rule1="POSTROUTING -t nat -s 192.168.122.0/24 ! -d 192.168.122.0/24 -j MASQUERADE"
rule2="PREROUTING -t nat -i eth0 -p tcp --dport 3128 -j DNAT --to-destination 192.168.122.10"
rule3="PREROUTING -t nat -i eth0 -p udp --dport 3128 -j DNAT --to-destination 192.168.122.10"

# Creation d'un pont reseau
brctl addbr proxybr
ifconfig proxybr up
ifconfig proxybr 192.168.122.1 netmask 255.255.255.0

# Creation d'une interface virtuelle pour la machine
tap=`tunctl -b -u root`

# Attachement de l'interface au pont
brctl addif proxybr $tap
ifconfig $tap up

# Activation de la translation d'adresse
echo 1 > /proc/sys/net/ipv4/ip_forward
iptables -A $rule1
iptables -A $rule2
iptables -A $rule3


# Lancement de la VM
kvm -m 512 /vservers/squid.raw -net nic,macaddr=DE:AD:BE:EF:44:40 -net tap,ifname=$tap,script=no

# Desactivation de la translation d'adresse
echo 0 > /proc/sys/net/ipv4/ip_forward
iptables -D $rule1
iptables -D $rule2
iptables -D $rule3

# Detachement de l'interface
brctl delif proxybr $tap
ifconfig $tap down

# Suppression de l'interface virtuelle
tunctl -d $tap

# Suppression du pont
ifconfig proxybr down
brctl delbr proxybr
#!/usr/bin/env python

import sys

def usage():
    print "proxy.py <port>"
    exit(1)

def main():
    pass

if __name__ == '__main__':
    if len(sys.argv)<2:
        usage()
    if not sys.argv[1].isdigit():
        usage()
    global __port__ = int(sys.argv[1])
    main()

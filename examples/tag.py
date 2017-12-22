# -*- coding: utf-8 -*-

import nfc
import binascii

def start_up(targets):
    print "start!!"
    print targets
    return targets

def on_connect(tag):
    # print tag
    # print tag.type
    print binascii.hexlify(tag.identifier).upper()
    return True

def on_release(tag):
    print "end!!"
    return True

def main():
    with nfc.ContactlessFrontend('usb') as clf:
        rdwr_option = {'on-startup': start_up,
                       'on-connect': on_connect,
                       'on-release': on_release,
                      }
        clf.connect(rdwr=rdwr_option)

if __name__ == '__main__':
    main()
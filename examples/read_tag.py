# -*- coding: utf-8 -*-

import nfc
import binascii

def on_connect(tag):
    # print tag
    # print tag.type
    print binascii.hexlify(tag.identifier).upper()

def main():
    with nfc.ContactlessFrontend('usb') as clf:
        clf.connect(rdwr={'on-connect': on_connect})

if __name__ == '__main__':
    main()
# -*- coding: utf-8 -*-

import nfc
import binascii


class TagReader(object):
    def __init__(self):
        self.tag_id = 0
        self.clf = nfc.ContactlessFrontend('usb')
        self.rdwr_option = {'on-connect': self.on_connect}

    def on_connect(self, tag):
        print "tag_id : ", binascii.hexlify(tag.identifier).upper()
        self.tag_id = binascii.hexlify(tag.identifier).upper()
        return True

    def read(self):
        self.clf.connect(rdwr=self.rdwr_option)
        return self.tag_id

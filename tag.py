# -*- coding: utf-8 -*-

import nfc
import binascii


class TagReager(object):
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


def read():
    reader = TagReager()
    reader.read()
    return reader.tag_id

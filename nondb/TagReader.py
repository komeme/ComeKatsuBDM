# -*- coding: utf-8 -*-

import nfc
import binascii


class TagReader(object):
    def __init__(self):
        self.state = 0
        self.tag_id = 0
        self.clf = nfc.ContactlessFrontend('usb')
        self.rdwr_option = {'on-startup': self.start_up,
                            'on-connect': self.on_connect,
                            'on-release': self.on_release,
                            }

    """
    state
    0 ... 待ち状態
    1 ... NFCチップを検索中
    2 ... NFCチップを検出している状態
    """

    def start_up(self, targets):
        print "start!!"
        print targets
        self.state = 1
        return targets

    def on_connect(self, tag):
        print "found!"
        print "tag_id : ", binascii.hexlify(tag.identifier).upper()
        self.state = 2
        self.tag_id = binascii.hexlify(tag.identifier).upper()
        return True

    def on_release(self, tag):
        print "end!!"
        self.state = 0
        return True

    def read(self):
        tag = self.clf.connect(rdwr=self.rdwr_option)
        return self.tag_id

if __name__ == '__main__':
    reader = TagReader()
    reader.read()
    print reader.state

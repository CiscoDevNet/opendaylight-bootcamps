'''
Created on Jan 22, 2016

@author: Bluesy Wang
'''

class EmbedderException(Exception):
    def __init__(self, code, msg):
        self.code = code
        self.msg = msg

    def __str__(self):
        return '%s (%s)' % (self.msg, self.code)
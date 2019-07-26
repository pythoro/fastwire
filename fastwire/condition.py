# -*- coding: utf-8 -*-
"""
Created on Sat Jul 27 08:58:09 2019

@author: Reuben
"""

class Condition():
    ''' A template for a signal condition '''
    name = 'default'
    def check(self, **kwargs):
        ''' The main check call - must return a boolean '''
        raise NotImplementedError()

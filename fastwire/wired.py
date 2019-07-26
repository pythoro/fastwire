# -*- coding: utf-8 -*-
"""
Created on Sat Jul 27 08:58:45 2019

@author: Reuben
"""

class Wired():
    def __new__(cls, *args, **kwargs):
        ''' Called at instance creation '''
        def register_signals(inst):
            try:
                sigs = inst.__getattribute__('_connected_signals')
                for name, s, receiver_kwargs in sigs:
                    s.connect(inst.__getattribute__(name), **receiver_kwargs)
            except AttributeError:
                pass
        
        inst = super().__new__(cls, *args, **kwargs)
        register_signals(inst)
        return inst
        
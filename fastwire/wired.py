# -*- coding: utf-8 -*-
"""
Created on Sat Jul 27 08:58:45 2019

@author: Reuben

This module provides mix-in classes to facilitate the decoration of methods.

"""

class Wired():
    ''' The mix-in class that enables method decoration to work '''
    
    def __new__(cls, *args, **kwargs):
        ''' Called at instance creation '''
        def register_signals(inst):
            try:
                sigs = inst.__getattribute__('_connected_signals')
                for name, s, box, container, receiver_kwargs in sigs:
                    if isinstance(s, str) or isinstance(s, int):
                        if box is not None:
                            s = box[s]
                        elif container is not None:
                            s = container[s]
                    s.connect(inst.__getattribute__(name), **receiver_kwargs)
            except AttributeError:
                pass
        
        try:
            inst = super().__new__(cls, *args, **kwargs)
        except TypeError:
            inst = super().__new__(cls)
        register_signals(inst)
        return inst
        
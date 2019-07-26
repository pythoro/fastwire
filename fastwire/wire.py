# -*- coding: utf-8 -*-
"""
Created on Sat Jul 27 08:57:12 2019

@author: Reuben
"""

class WireContainer(dict):
    ''' Holds a collection of signals '''
    
    def wire(self, name=None, doc=None):
        name = len(self) if name is None else name
        w = Wire(name=name, doc=doc)
        self[name] = w
        return w
    
    def mute_all(self):
        for key, wire in self.items():
            wire.mute()

    def unmute_all(self):
        for key, wire in self.items():
            wire.unmute()

    def reset_all(self):
        for key, wire in self.items():
            wire.reset()
    

default_wire_container = WireContainer()
wire = default_wire_container.wire


class Wire():
    def __init__(self, name=None, doc=None):
        self._name = name
        self._doc = doc
        self.reset()
        
    def _emit(self):
        raise AttributeError('Wire instance is not connected')
    
    def connect(self, receiver):
        if self.emit != self._emit:
            raise AttributeError('Wire instance is already connected and'
                                 + 'must first be disconnected.')
        self.emit = receiver
        self.fetch = receiver
    
    def disconnect(self):
        self.reset()
        
    def _muted(self):
        pass
        
    def mute(self):
        self._old = self.emit
        self.emit = self._muted

    def unmute(self):
        self.emit = self._old
        del self._old
        
    def reset(self):
        self.emit = self._emit
        self.fetch = self._emit
        

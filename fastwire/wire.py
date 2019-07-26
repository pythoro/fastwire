# -*- coding: utf-8 -*-
"""
Created on Sat Jul 27 08:57:12 2019

@author: Reuben

The wire module is about simple 'Wire' classes. Wire instances can be connected
to one, and only one, receiver (a callable). Unlike Signals, Wire instances
hold normal a normal reference to the callable.

"""

class WireContainer(dict):
    ''' A dictionary-like collection of Wire instances '''
    
    def wire(self, name=None, doc=None):
        ''' Get a new Wire instance 
        
        Args:
            name (str): A name of the wire [optional]
            doc (str): A documentation string for the wire [optional]
        '''
        name = len(self) if name is None else name
        w = Wire(name=name, doc=doc)
        self[name] = w
        return w
    
    def mute_all(self):
        ''' Mute all wires in the container '''
        for key, wire in self.items():
            wire.mute()

    def unmute_all(self):
        ''' Unmute all wires in the container '''
        for key, wire in self.items():
            wire.unmute()

    def reset_all(self):
        ''' Reset all wires in the contain '''
        for key, wire in self.items():
            wire.reset()
    

default_wire_container = WireContainer()
wire = default_wire_container.wire


class Wire():
    ''' A simple instance that can be connected to one receiver 
    
        Args:
            name (str): A name of the wire [optional]
            doc (str): A documentation string for the wire [optional]    
    '''
    
    def __init__(self, name=None, doc=None):
        self._name = name
        self._doc = doc
        self.reset()
        
    def _emit(self):
        ''' The default, unconnected, method '''
        raise AttributeError('Wire instance is not connected')
    
    def connect(self, receiver):
        ''' Connect the wire to a callable receiver 
        
        Args:
            receiver (callable): A receiver called by the wire.
        '''
        if self.emit != self._emit:
            raise AttributeError('Wire instance is already connected and'
                                 + 'must first be disconnected.')
        self.emit = receiver
        self.fetch = receiver
    
    def disconnect(self):
        ''' Disconnect the wire from its receiver '''
        self.reset()
        
    def _muted(self):
        ''' The default muted method '''
        pass
        
    def mute(self):
        ''' Prevent the wire from calling the receiver '''
        self._old = self.emit
        self.emit = self._muted

    def unmute(self):
        ''' Allow the wire to call the receiver '''
        self.emit = self._old
        del self._old
        
    def reset(self):
        ''' Fully reset the wire, disconnecting it if required '''
        self.emit = self._emit
        self.fetch = self._emit
        

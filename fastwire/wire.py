# -*- coding: utf-8 -*-
"""
Created on Sat Jul 27 08:57:12 2019

@author: Reuben

The wire module is about simple 'Wire' classes. Wire instances can be connected
to one, and only one, receiver (a callable). Unlike Signals, Wire instances
hold normal a normal reference to the callable.

"""

import warnings

from . import box, container
from . import settings


class Wire():
    ''' A simple instance that can be connected to one receiver 
    
        Args:
            name (str): A name of the wire [optional]
            doc (str): A documentation string for the wire [optional]    
            **attributes: Optional key word arguments, which are stored
                as attributes of the signal.

    '''
    
    def __init__(self, name=None, doc=None, attrs=None, **kwargs):
        self._name = name
        self._doc = doc
        self._receiver_limit = 1
        self._attrs = attrs
        self.reset()
        
    def _emit(self, *args, **kwargs):
        ''' The default, unconnected, method '''
        raise AttributeError('Wire instance is not connected')
    
    def connect(self, receiver):
        ''' Connect the wire to a callable receiver 
        
        Args:
            receiver (callable): A receiver called by the wire.
        '''
        if self.emit != self._emit:
            if settings.WARN_WIRE_RECONNECT:
                warnings.warn('FASTWIRE: Wire "' + str(self.name)
                + '" was already connected to ' + str(self.emit)
                + ' and was reconnected to ' + str(receiver) + '. Use a Signal'
                + ' if multiple connections are required.', stacklevel=2)
        self.emit = receiver
        self.fetch = receiver
        self.receivers_present = True
    
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
        self.receivers_present = False
        
    @property
    def name(self):
        ''' The wire name '''
        return self._name

    @property
    def doc(self):
        ''' The wire documentation '''
        return self._doc

    @property
    def attrs(self):
        ''' The wire documentation '''
        return self._attrs


class WireContainer(container.Container):
    ''' A dictionary-like collection of Signal instances '''
    
    def __init__(self, cid=None):
        super().__init__(signal_cls=Wire, cid=cid)
        
    def wire(self, name=None, doc=None, attrs=None, **kwargs):    
        ''' Create or get a new wire instance
        
        Args:
            name (str): A name of the wire/signal [optional]
            doc (str): A documentation string for the wire/signal [optional]
            attrs (dict): Optional diction of signal attributes.
        '''
        return self.get(name=name, doc=doc, attrs=attrs, **kwargs)

    
class WireBox(box.Box):
    ''' A collection of SignalContainers'''
    
    def __init__(self):
        super().__init__(container_cls=WireContainer)
    
    def wire(self, name=None, doc=None, attrs=None, **kwargs):
        ''' Create or get a new signal instancein the active container
        
        Args:
            name (str): A name of the wire/signal [optional]
            doc (str): A documentation string for the wire/signal [optional]
            attrs (dict): Optional diction of signal attributes.
        '''
        return self.get(name=name, doc=doc, attrs=attrs, **kwargs)


wire_boxes = {}

def wire_box(name):
    if name not in wire_boxes:
        wire_boxes[name] = WireBox()
    return wire_boxes[name]

def wire_container(name):
    box = wire_box('default')
    return box.get_container(name)

default_wire_box = wire_box('default')
default_wire_container = wire_container('default')
wire = default_wire_container.wire

# -*- coding: utf-8 -*-
"""
Created on Wed Jul 31 12:56:25 2019

@author: Reuben
"""

import weakref
import functools

from . import decorate

class Box():
    ''' A collection of containers 
    
    It's used to allow client classes to create sets of signals for specific
    instances. Other classes instantiated can call an instance of this class
    to get signals within the appropriate set. This can help to avoid
    signals getting mixed up.
    '''
    def __init__(self, container_cls):
        self._container_cls = container_cls
        self._cs = {}
        self.add('default')
        self.receive = functools.partial(decorate.receive, box=self)
        self.supply = functools.partial(decorate.supply, box=self)
        
    @property
    def containers(self):
        return self._cs
        
    def add(self, cid, activate=True, remove_with=None):
        ''' Add a new container referenced with cid
        
        Args:
            cid (int, str): A reference for the container
            activate (bool): Set the container as the active one
            remove_with (object): An object to associate the container with.
                When the object is garbage collected, its container and
                all signals within it will also be removed. This can be useful
                to avoid objects accumulating in memory.
        '''
        c = self._container_cls()
        self._cs[cid] = c
        if remove_with is not None:
            weakref.finalize(remove_with, self.remove, cid=cid)
        if activate:
            self.set_active(cid)
        return c
        
    def remove(self, cid):
        ''' Remove a container
        
        Note:
            This sets the active container to 'default'.
        
        Args:
            cid (int, str): The container reference '''
        del self._cs[cid]
        self.set_active('default')
        
    def set_active(self, cid):
        ''' Set the active container 
        
        Args:
            cid(int, str): The container reference
        '''
        self._active = cid
        
    def get_active(self):
        ''' Return the currently active container '''
        if self._active is None:
            return None
        return self._cs[self._active]
        
    def new(self, name=None, doc=None, **kwargs):
        ''' Create a new wire/signal instance in the currently active container
        
        Args:
            name (str): A name of the wire/signal [optional]
            doc (str): A documentation string for the wire/signal [optional]
            **kwargs: Optional key word arguments.
        '''
        c = self.get_active()
        return c.new(name=name, doc=doc, **kwargs)
    
    def __getitem__(self, name):
        ''' Get or create a signal in the currently active container '''
        c = self.get_active()
        return c[name]
    
    def reset_all(self):
        ''' Reset all wires in the contain '''
        for key, container in self._cs.items():
            container.reset_all()
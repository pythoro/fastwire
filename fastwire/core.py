# -*- coding: utf-8 -*-
"""
Created on Sun Jul 21 21:59:00 2019

@author: reube
"""

import weakref

class SignalContainer(dict):

    def signal(self, name=None):
        name = len(self) if name is None else name
        s = Signal(name=name)
        self[name] = s
        return s
    
default_container = SignalContainer()
signal = default_container.signal

    
class Signal():
    def __init__(self, name=None, receiver_limit=None):
        self._receivers = {}
        self._receiver_kwargs = {}
        self._name = name
        self._receiver_limit = receiver_limit
        self._next_id = 0
    
    def connect(self, receiver, **receiver_kwargs):
        if self.n == self._receiver_limit:
            raise KeyError('Limit of receivers (or suppliers) reached.')
        receiver_id = self._next_id
        if hasattr(receiver, '__self__') and hasattr(receiver, '__func__'):
            ref = weakref.WeakMethod(receiver)
            obj = receiver.__self__
        else:
            ref = weakref.ref(receiver)
            obj = receiver
        self._receivers[receiver_id] = ref
        self._receiver_kwargs[receiver_id] = receiver_kwargs
        weakref.finalize(obj, self.disconnect, receiver_id)
        self._next_id += 1
        return receiver_id
    
    @property
    def n(self):
        return len(self._receivers)

    @property
    def receivers_present(self):
        return len(self._receivers) > 0
    
    @property
    def name(self):
        return self._name
    
    def disconnect(self, receiver_id):
        try:
            del self._receivers[receiver_id]
            del self._receiver_kwargs[receiver_id]
        except KeyError:
            pass
        return True
    
    def emit(self, **kwargs):
        for receiver_id, ref in self._receivers.items():
            receiver = ref()
            receiver(**kwargs)
            
    def fetch(self, **kwargs):
        if self._receiver_limit != 1:
            raise KeyError('Signal must be set to have only 1 supplier.')
        if self.n == 0:
            raise KeyError('No suppliers')
        for receiver_id, ref in self._receivers.items():
            receiver = ref()
            return receiver(**kwargs)


def connect_to(s, **receiver_kwargs):
    if not isinstance(s, list):
        s = [s]
        
    class Decorator():
        # See https://stackoverflow.com/questions/2366713/can-a-python-decorator-of-an-instance-method-access-the-class
        def __init__(self, fn):
            self.fn = fn
    
        def __set_name__(self, owner, name):
            # Called at class creation
            for signal in s:
                signal.connect(self.fn, **receiver_kwargs)
            setattr(owner, name, self.fn)
    return Decorator


def supplies(s, **receiver_kwargs):
        if s._receiver_limit != 1:
            raise KeyError('Signal must be set to have only 1 supplier.')
        return connect_to(s, **receiver_kwargs)

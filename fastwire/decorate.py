# -*- coding: utf-8 -*-
"""
Created on Sat Jul 27 08:58:26 2019

@author: Reuben
"""


def receive(s, **receiver_kwargs):
    ''' A decorator to connect functions and methods automatically '''
    if not isinstance(s, list):
        s = [s]
        
    class Decorator():
        # See https://stackoverflow.com/questions/2366713/can-a-python-decorator-of-an-instance-method-access-the-class
        def __init__(self, fn):
            self.fn = fn
    
        def __set_name__(self, owner, name):
            # Called at class creation
            if not hasattr(owner, '_connected_signals'):
                owner._connected_signals = []
            cs = owner._connected_signals
            for signal in s:
                cs.append([name, signal, receiver_kwargs])
            setattr(owner, name, self.fn) # Replace decorator with original function
        
    return Decorator


def supply(s, **receiver_kwargs):
    ''' A special case of reciever where there must be only one source '''
    if s._receiver_limit != 1:
        raise KeyError('Signal must be set to have only 1 supplier.')
    return receive(s, **receiver_kwargs)


def fn_receive(s, **receiver_kwargs):
    ''' For functions '''
    if not isinstance(s, list):
        s = [s]
    def decorator(fn):
        for signal in s:
            signal.connect(fn, **receiver_kwargs)
        return fn
    return decorator


def fn_supply(s, **receiver_kwargs):
    if s._receiver_limit != 1:
        raise KeyError('Signal must be set to have only 1 supplier.')
    return fn_receive(s, **receiver_kwargs)

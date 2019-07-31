# -*- coding: utf-8 -*-
"""
Created on Sat Jul 27 08:56:13 2019

@author: Reuben

Signals can be connected to multiple callable receivers. The hold weak
references to those callables, so that when they are garbage collected their
references are removed automatically.

"""


import weakref


class SignalBox():
    ''' A collection of SignalContainers 
    
    It's used to allow client classes to create sets of signals for specific
    instances. Other classes instantiated can call an instance of this class
    to get signals within the appropriate set. This can help to avoid
    signals getting mixed up.
    '''
    def __init__(self):
        self._scs = {}
        self._active = None
        
    def add(self, cid, activate=True, remove_with=None):
        ''' Add a new SignalContainer referenced with cid
        
        Args:
            cid (int, str): A reference for the container
            activate (bool): Set the container as the active one
            remove_with (object): An object to associate the container with.
                When the object is garbage collected, its container and
                all signals within it will also be removed. This can be useful
                to avoid objects accumulating in memory.
        '''
        sc = SignalContainer()
        self._scs[cid] = sc
        if remove_with is not None:
            weakref.finalize(remove_with, self.remove, cid=cid)
        if activate:
            self.set_active(cid)
        return sc
        
    def remove(self, cid):
        ''' Remove a container 
        
        Args:
            cid (int, str): The container reference '''
        del self._scs[cid]
        
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
        return self._scs[self._active]
        
    def signal(self, name=None, doc=None, **kwargs):
        ''' Create a Signal instance in the currently active container
        
        Args:
            name (str): A name of the wire [optional]
            doc (str): A documentation string for the wire [optional]
        '''
        cs = self.get_active()
        return cs.signal(name=name, doc=doc, **kwargs)
    
    def __getitem__(self, name):
        ''' Get or create a signal in the currently active container '''
        cs = self.get_active()
        return cs[name]
    

class SignalContainer(dict):
    ''' A dictionary-like collection of Signal instances '''
    
    def signal(self, name=None, doc=None, **kwargs):
        ''' Get a new Signal instance 
        
        Args:
            name (str): A name of the wire [optional]
            doc (str): A documentation string for the wire [optional]
        '''
        name = len(self) if name is None else name
        s = Signal(name=name, doc=doc, **kwargs)
        self[name] = s
        return s
    
    def mute_all(self):
        ''' Mute all signals in the container '''
        for key, signal in self.items():
            signal.mute()

    def unmute_all(self):
        ''' Unmute all signals in the container '''
        for key, signal in self.items():
            signal.unmute()

    def reset_all(self):
        ''' Reset all wires in the contain '''
        for key, signal in self.items():
            signal.reset()
    
    def __getitem__(self, name):
        ''' Get or create a Signal instance 
        
        Args:
            key: The name of the signal
        '''
        if name in self:
            return super().__getitem__(name)
        else:
            s = Signal(name=name)
            super().__setitem__(name, s)
            return s
            
    
default_container = SignalContainer()
signal = default_container.signal

    
class Signal():
    ''' A class that can emit and receive data from multiple callables. 
    
        Args:
            name (str): A name of the wire [optional]
            doc (str): A documentation string for the wire [optional]
            receiver_limit (int): Limit the number of receivers [optional]
            condition (Condition): An optional signal Condition.
    '''
    
    def __init__(self, name=None, doc=None, receiver_limit=None, condition=None):
        self.reset()
        self._name = name
        self._doc = doc
        self._receiver_limit = receiver_limit
        if condition is not None:
            self.add_condition(condition)
    
    def add_condition(self, condition):
        ''' Add a condition that the signal must pass to be received
        
        Args:
            condition (Condition): A Condition instance
        '''
        self._conditions[condition.name] = condition
        self.emit = self._conditioned_emit
        return True
        
    def remove_condition(self, name):
        ''' Remove a condition that the signal must pass to be received 
        
        Args:
            name (str): The name of the condition to remove.
        '''
        try:
            del self._conditions[name]
        except KeyError:
            pass
        if len(self._conditions) == 0:
            self.emit = self._emit
    
    def connect(self, receiver, **receiver_kwargs):
        ''' Store weakref of receiver function or method to call 
        
        Args:
            receiver (callable): A callable receiver
            kwargs: Optional key word arguments
            
        Returns:
            float: A receiver id that can be used to disconnect
        '''
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
        ''' Number of recievers '''
        return len(self._receivers)

    @property
    def receivers_present(self):
        ''' A boolean check if receivers are present '''
        return len(self._receivers) > 0
    
    @property
    def name(self):
        ''' The signal name '''
        return self._name
    
    def disconnect(self, receiver_id):
        ''' Disconnect a receiver 
        
        Args:
            receiver_id (int): The id of the receiver.
        '''
        try:
            del self._receivers[receiver_id]
            del self._receiver_kwargs[receiver_id]
        except KeyError:
            pass
        return True

    def _emit(self, **kwargs):
        ''' The standard emit method 

        Args:
            **kwargs: Key word arguments.
        
        Note: The 'emit' method is set to this method normally.
        '''
        for receiver_id, ref in self._receivers.items():
            receiver = ref()
            receiver(**kwargs)
            
    def _conditioned_emit(self, **kwargs):
        ''' A conditioned emit method 
        
        Args:
            **kwargs: Key word arguments.
        '''
        for receiver_id, ref in self._receivers.items():
            condition_pass = True
            for condition_name, condition in self._conditions.items():
                rec_kwargs = self._receiver_kwargs[receiver_id]
                all_kwargs = {**rec_kwargs, **kwargs}
                condition_pass &= condition.check(**all_kwargs)
            if condition_pass:
                self._emit(**kwargs)

    def _muted(self, **kwargs):
        pass
            
    def mute(self):
        ''' Prevent receivers from receiving signals '''
        self._prev_emit = self.emit
        self.emit = self._muted

    def unmute(self):
        ''' Allow receivers to receive signals (after a mute) '''
        self.emit = self._prev_emit
        del self._prev_emit
    
    def fetch(self, **kwargs):
        ''' Get a return value from a single supplier 
        
        Args:
            **kwargs: Key word arguments.
        '''
        if self._receiver_limit != 1:
            raise KeyError('Signal must be set to have only 1 supplier.')
        if self.n == 0:
            raise KeyError('No suppliers')
        for receiver_id, ref in self._receivers.items():
            receiver = ref()
            return receiver(**kwargs)

    def fetch_all(self, **kwargs):
        ''' Get return value from all connected callables 
        
        Args:
            **kwargs: Key word arguments.        
        
        Returns:
            list: The list of return values
        '''
        if self.n == 0:
            raise KeyError('No suppliers')
        ret = []
        for receiver_id, ref in self._receivers.items():
            receiver = ref()
            ret.append(receiver(**kwargs))
        return ret

    def reset(self):
        ''' Reset the signal '''
        self._receivers = {}
        self._receiver_kwargs = {}
        self._next_id = 0
        self._conditions = {}
        self.emit = self._emit

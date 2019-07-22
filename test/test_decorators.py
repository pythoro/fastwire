# -*- coding: utf-8 -*-
"""
Created on Sun Jul 21 22:47:12 2019

@author: Reuben
"""

import fastwire

import unittest


class Test_Decorators(unittest.TestCase):
    
    def test_method_connect_to(self):
        signal = fastwire.Signal()

        class A(fastwire.Fastwired):
            @fastwire.connect_to(signal)
            def connected(self, a):
                self._a = a

        a = A()
        self.assertEqual(len(signal._receivers.keys()), 1)

        
    def test_method_supplies(self):
        signal = fastwire.Signal(receiver_limit=1)

        class A(fastwire.Fastwired):
            @fastwire.supplies(signal)
            def connected(self, a):
                self._a = a

        a = A()
        self.assertEqual(len(signal._receivers.keys()), 1)

        
    def test_method_connect_to_emit(self):
        signal = fastwire.Signal()

        class A(fastwire.Fastwired):
            @fastwire.connect_to(signal)
            def connected(self, a):
                self._a = a

        a = A()
        val = 5.7
        signal.emit(a=val)
        self.assertEqual(a._a, val)

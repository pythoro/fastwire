# -*- coding: utf-8 -*-
"""
Created on Thu Jul 25 09:22:35 2019

@author: Reuben
"""

import fastwire

import unittest

class Test_Wire(unittest.TestCase):
    
    def test_method_emit(self):
        wire = fastwire.Wire()

        class A():
            def connected(self, a):
                self._a = a
                return a

        a = A()
        wire.connect(a.connected)
        wire.emit(5)
        self.assertEqual(a._a, 5)
# -*- coding: utf-8 -*-
"""
Created on Sun Jul 21 22:46:33 2019

@author: Reuben
"""

import fastwire

import unittest


class Test_SignalBox(unittest.TestCase):
    
    def test_create(self):
        sb = fastwire.SignalBox()
        sc = sb.add(id(self))
        self.assertEqual(sb.__class__, fastwire.SignalBox)
        
    def test_activate(self):
        sb = fastwire.SignalBox()
        sc = sb.add(id(self))
        sc2 = sb.add(3049)
        sb.set_active(id(self))
        sc_check = sb.get_active()
        self.assertEqual(sc, sc_check)
        
    def test_create_signal(self):
        sb = fastwire.SignalBox()
        sc = sb.add(id(self))
        signal = sb.signal('this_name')
        self.assertEqual(signal.name, 'this_name')
        self.assertEqual(signal.__class__, fastwire.Signal)

    def test_create_on_demand(self):
        sb = fastwire.SignalBox()
        sc = sb.add(id(self))
        signal = sb['this_name']
        self.assertEqual(signal.name, 'this_name')
        self.assertEqual(signal.__class__, fastwire.Signal)

    def test_remove(self):
        sb = fastwire.SignalBox()
        sb.add(0)
        self.assertEqual(len(sb._cs), 2)
        sb.remove(0)
        self.assertEqual(len(sb._cs), 1)
        
    def test_remove_with(self):
        class A():
            pass
        a = A()
        sb = fastwire.SignalBox()
        sb.add(id(a), remove_with=a)
        self.assertEqual(len(sb._cs), 2)
        del a
        self.assertEqual(len(sb._cs), 1)

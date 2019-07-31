# -*- coding: utf-8 -*-
"""
Created on Sun Jul 21 22:46:33 2019

@author: Reuben
"""

import fastwire

import unittest


class Test_WireBox(unittest.TestCase):
    
    def test_create(self):
        wb = fastwire.WireBox()
        wc = wb.add(id(self))
        self.assertEqual(wb.__class__, fastwire.WireBox)
        
    def test_activate(self):
        wb = fastwire.WireBox()
        wc = wb.add(id(self))
        sc2 = wb.add(3049)
        wb.set_active(id(self))
        sc_check = wb.get_active()
        self.assertEqual(wc, sc_check)
        
    def test_create_wire(self):
        wb = fastwire.WireBox()
        wc = wb.add(id(self))
        wire = wb.wire('this_name')
        self.assertEqual(wire.name, 'this_name')
        self.assertEqual(wire.__class__, fastwire.Wire)

    def test_create_on_demand(self):
        wb = fastwire.WireBox()
        wc = wb.add(id(self))
        wire = wb['this_name']
        self.assertEqual(wire.name, 'this_name')
        self.assertEqual(wire.__class__, fastwire.Wire)

    def test_remove(self):
        wb = fastwire.WireBox()
        wb.add(0)
        self.assertEqual(len(wb._scs), 1)
        wb.remove(0)
        self.assertEqual(len(wb._scs), 0)
        
    def test_remove_with(self):
        class A():
            pass
        a = A()
        wb = fastwire.WireBox()
        wb.add(id(a), remove_with=a)
        self.assertEqual(len(wb._scs), 1)
        del a
        self.assertEqual(len(wb._scs), 0)

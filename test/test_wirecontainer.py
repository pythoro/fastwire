# -*- coding: utf-8 -*-
"""
Created on Wed Jul 31 12:38:18 2019

@author: Reuben
"""

import fastwire

import unittest


class Test_WireContainer(unittest.TestCase):
    
    def test_unnamed_wire(self):
        sc = fastwire.WireContainer()
        wire = sc.wire()
        self.assertEqual(wire.__class__, fastwire.Wire)
        
    def test_named_wire(self):
        sc = fastwire.WireContainer()
        wire = sc.wire('this_name')
        self.assertEqual(wire.name, 'this_name')

    def test_create_on_demand(self):
        sc = fastwire.WireContainer()
        wire = sc['this_name']
        self.assertEqual(wire.name, 'this_name')
        self.assertEqual(wire.__class__, fastwire.Wire)
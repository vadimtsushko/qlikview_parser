#!/usr/bin/env python
# -*- coding: utf-8 -*-

import re
import sys
import unittest
import tpg
from tpg_qv import ExpressionParser

class LexerOptionsTestCase(unittest.TestCase):
  def __init__(self, *args, **kwargs):
    super(LexerOptionsTestCase, self).__init__(*args, **kwargs)
    self.parser = ExpressionParser()
  def checkParse(self,expr,start = 'START'):
    error = None
    try:
        expr = self.parser.parse(start, expr)
    except tpg.Error:
        error = tpg.exc()
    self.assertEqual(None,error, 'Parse should pass')
    
  def testSimple(self):
    self.checkParse('1+2\n\n')
    expr = """1+
          2

          """
    #self.assertIsInstance('%s' % p(expr), str)
    #self.assertRaises(tpg.SyntacticError,p,expr)
    #self.assertIsInstance('%s' % p("a + min(total<Начало, Start> 'asd', 3 , 5)"), str,"Expression can be terminated withour line break")
    self.checkParse(expr)



try:
    unittest.main()
except SystemExit:
    if tpg.exc().args[0]:
        raise

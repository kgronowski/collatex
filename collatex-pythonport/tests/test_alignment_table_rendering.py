'''
Created on Jun 11, 2014

@author: Ronald Haentjens Dekker
'''
import unittest
from collatex.core_functions import Collation, collate


class Test(unittest.TestCase):

    def testPlainTableRendering(self):
        collation = Collation()
        collation.add_witness("A", "This very quick very quick brown wombat")
        collation.add_witness("B", "That very quick brown koala")
        collation.add_witness("C", "That very quick brown kangaroo")
        expected_output = """+---+-----------------+------------------+----------+
| A | This very quick | very quick brown | wombat   |
| B | That            | very quick brown | koala    |
| C | That            | very quick brown | kangaroo |
+---+-----------------+------------------+----------+"""
        plain_text_output = str(collate(collation))
        self.assertEquals(expected_output, plain_text_output)

    def testPlainTableRenderingNoParallelSegmentation(self):
        collation = Collation()
        collation.add_witness("A", "This very quick very quick brown wombat")
        collation.add_witness("B", "That very quick brown koala")
        collation.add_witness("C", "That very quick brown kangaroo")
        expected_output = """+---+------+------+-------+------+-------+-------+----------+
| A | This | very | quick | very | quick | brown | wombat   |
| B | That | -    | -     | very | quick | brown | koala    |
| C | That | -    | -     | very | quick | brown | kangaroo |
+---+------+------+-------+------+-------+-------+----------+"""
        plain_text_output = str(collate(collation, segmentation=False))
        self.assertEquals(expected_output, plain_text_output)

    def testJSONAlignmentTableRendering(self):
        collation = Collation()
        collation.add_witness("A", "This very quick very quick brown wombat")
        collation.add_witness("B", "That very quick brown koala")
        collation.add_witness("C", "That very quick brown kangaroo")
        expected_output = '{"table": [[["This very quick"], ["very quick brown"], ["wombat"]], [["That"], ["very quick brown"], ["koala"]], [["That"], ["very quick brown"], ["kangaroo"]]], "witnesses": ["A", "B", "C"]}'
        json = collate(collation, output="json")
        self.assertEquals(expected_output, json)

    def testColumnStatusInAlignmentTable(self):
        collation = Collation()
        collation.add_witness("A", "The quick brown fox jumps over the dog.")
        collation.add_witness("B", "The brown fox jumps over the lazy dog.")
        alignment_table = collate(collation)
        status_array = []
        for column in alignment_table.columns:
            status_array.append(column.variant)
        self.assertEqual([False, True, False, True, False], status_array)
        collation.add_witness("C", "The brown fox walks around the lazy dog.")
        collate(collation)    
        alignment_table = collate(collation)
        status_array = []
        for column in alignment_table.columns:
            status_array.append(column.variant)
        self.assertEqual([False, True, False, True, False, True, False], status_array)
        
if __name__ == "__main__":
    #import sys;sys.argv = ['', 'Test.testName']
    unittest.main()
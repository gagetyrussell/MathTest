# -*- coding: utf-8 -*-
"""
Created on Tue Dec 22 12:48:54 2020

@author: Owner
"""
import sys
sys.path.append('../')

from MathTest import MathTest

import unittest 
import re
 
class test_MathTest(unittest.TestCase):
    
    def setUp(self):
        
        self.setup_operators = ['addition', 'multiplication', 'subtraction', 'division']
        self.setup_test_length = 10
        self.math_test = MathTest(operators=self.setup_operators, test_length=self.setup_test_length) 
        self.addition_regex = re.compile('\d+ \+ \d+')
        self.subtraction_regex = re.compile('\d+ \- \d+')
        self.multiplication_regex = re.compile('\d+ \* \d+')
        self.division_regex = re.compile('\d+ \/ \d+')
 
    def test_initialization(self):  
        
        self.assertEqual(self.math_test.operators, self.setup_operators)
        self.assertEqual(self.math_test.test_length, self.setup_test_length)
        
    def test_non_supported_operators_initialization(self):  
        operators = ['I am unsupported']
        
        with self.assertRaises(Exception) as context:
            math_test = MathTest(operators=operators, test_length=10) 
            self.assertTrue('Unsupported Operators' in context.exception)        
        
        
    def test_prompt_operator(self):
        
        response = self.math_test.prompt_operator()  
        self.assertEqual(self.math_test.selected_operator, response)     
        
    def test_length_of_questions(self):
        
        self.math_test.selected_operator = 'addition'
        self.assertEqual(self.math_test.selected_operator, 'addition')   
        
        questions = self.math_test.generate_questions()
        
        self.assertEqual(len(questions), self.math_test.test_length) 
        
    def test_question_reset(self):
        
        self.math_test.selected_operator = 'addition'
        self.assertEqual(self.math_test.selected_operator, 'addition') 
        
        questions = self.math_test.generate_questions()
        
        self.math_test.reset_questions()
        
        self.assertEqual(self.math_test.questions, [])
        
    def test_regex_of_addition_questions(self):
        
        operator = 'addition'
        self.math_test.selected_operator = operator
        self.assertEqual(self.math_test.selected_operator, operator) 
        
        questions = self.math_test.generate_questions()
        
        check = all([self.addition_regex.fullmatch(q['question_string']) for q in questions])
        
        self.assertTrue(check)        
        
    def test_regex_of_subtraction_questions(self):
        
        operator = 'subtraction'
        self.math_test.selected_operator = operator
        self.assertEqual(self.math_test.selected_operator, operator) 
        
        questions = self.math_test.generate_questions()
        
        check = all([self.subtraction_regex.fullmatch(q['question_string']) for q in questions])
        
        self.assertTrue(check)     
        
    def test_regex_of_multiplication_questions(self):
        
        operator = 'multiplication'
        self.math_test.selected_operator = operator
        self.assertEqual(self.math_test.selected_operator, operator) 
        
        questions = self.math_test.generate_questions()
        
        check = all([self.multiplication_regex.fullmatch(q['question_string']) for q in questions])
        
        self.assertTrue(check) 
        
    def test_regex_of_division_questions(self):
        
        operator = 'division'
        self.math_test.selected_operator = operator
        self.assertEqual(self.math_test.selected_operator, operator) 
        
        questions = self.math_test.generate_questions()
        
        check = all([self.division_regex.fullmatch(q['question_string']) for q in questions])
        
        self.assertTrue(check) 
        
    def test_addition_answers(self):
        operator = 'addition'
        self.math_test.selected_operator = operator
        self.assertEqual(self.math_test.selected_operator, operator) 
        
        questions = self.math_test.generate_questions()
        
        check = all([eval(q['question_string']) == q['answer'] for q in questions])
        
        self.assertTrue(check) 
        
    def test_subtraction_answers(self):
        operator = 'subtraction'
        self.math_test.selected_operator = operator
        self.assertEqual(self.math_test.selected_operator, operator) 
        
        questions = self.math_test.generate_questions()
        
        check = all([eval(q['question_string']) == q['answer'] for q in questions])
        
        self.assertTrue(check) 
        
    def test_multiplication_answers(self):
        operator = 'multiplication'
        self.math_test.selected_operator = operator
        self.assertEqual(self.math_test.selected_operator, operator) 
        
        questions = self.math_test.generate_questions()
        
        check = all([eval(q['question_string']) == q['answer'] for q in questions])
        
        self.assertTrue(check) 
        
    def test_division_answers(self):
        operator = 'division'
        self.math_test.selected_operator = operator
        self.assertEqual(self.math_test.selected_operator, operator) 
        
        questions = self.math_test.generate_questions()
        
        check = all([eval(q['question_string']) == q['answer'] for q in questions])
        
        self.assertTrue(check) 
        
        
 
        
        

        
        
         
 
    # def test_stop(self):
 
    #     self.car.speed = 5
 
    #     self.car.stop()
 
    #     # Verify the speed is 0 after stopping
 
    #     self.assertEqual(0, self.car.speed)
 
         
 
    #     # Verify it is Ok to stop again if the car is already stopped
 
    #     self.car.stop()
 
    #     self.assertEqual(0, self.car.speed)
        
if __name__ == '__main__':
    print('here')
    unittest.main()
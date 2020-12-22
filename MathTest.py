# -*- coding: utf-8 -*-
"""
Created on Mon Dec 21 19:17:36 2020

@author: Owner
"""

# the code used to get a random non-prime number is stollen directly from StackExchange
# https://stackoverflow.com/questions/38416864/generating-a-random-non-prime-number-in-python
# Further, it was stolen in the answer:
# https://jeremykun.com/2013/06/16/miller-rabin-primality-test/
from helpers import get_random_nonprime, divisor_generator

#from prompt_toolkit.validation import Validator, ValidationError
from PyInquirer import style_from_dict, Token, prompt, Separator
from pprint import pprint
from random import randint

class MathTest():
        
    def __init__(self, operators: list, test_length=10) -> str:
        
        self.supported_operators = {'addition': '+',
                                    'multiplication': '*',
                                    'subtraction': '-',
                                    'division': '/'}
        
        if not all([op in self.supported_operators.keys() for op in operators]):
            raise ValueError('Unsupported Operators')
        
        self.operators = operators
        self.test_length = test_length
        self.style = style_from_dict({
            Token.Separator: '#cc5454',
            Token.QuestionMark: '#673ab7 bold',
            Token.Selected: '#cc5454',  # default
            Token.Pointer: '#673ab7 bold',
            Token.Instruction: '',  # default
            Token.Answer: '#f44336 bold',
            Token.Question: '',
        })
        self.selected_operator = None
        self.questions = []
        self.answers = []
        self.score = None
        self.proceed_options = ['retry', 'new test', 'quit']
        self.selected_proceed = None
        
    def prompt_operator(self):
        
        operator_question = {
            'type': 'list',
            'name': 'operator_selection',
            'message': 'Select the arithmetic operation you would like to be tested on:',
            'choices': [{'name': op} for op in self.operators]
        }
        
        operator_response = prompt(operator_question, style=self.style)
        self.selected_operator = operator_response['operator_selection']
        
        return operator_response['operator_selection']
        
    def get_numbers(self):
        if self.selected_operator == 'division':
            # we cannot have a prime number
            first_number = get_random_nonprime(0,100)
            second_number_possibilities = [i for i in divisor_generator(first_number)]
            second_number_index = randint(0, len(second_number_possibilities)-1)
            second_number = second_number_possibilities[second_number_index]
            
        elif self.selected_operator == 'addition':
            first_number = randint(0, 10)
            second_number = randint(0, 10)
            
        elif self.selected_operator == 'multiplication':
            first_number = randint(0, 10)
            second_number = randint(0, 10)
            
        elif self.selected_operator == 'subtraction':
            first_number = randint(0, 10)
            second_number = randint(0, first_number)
            
        else:
            raise ValueError('Unsupported Operators')
            
        return (first_number, second_number)
    
    def generate_question(self):
        number = self.get_numbers()
        question_string = f"{number[0]} {self.supported_operators[self.selected_operator]} {number[1]}"
        answer = eval(question_string)
        
        question_dict = dict(question_string=question_string, answer=answer)
        
        return question_dict
            
    def generate_questions(self):

        for i in range(self.test_length):
            self.questions.append(self.generate_question())
            
        return self.questions
            
    def ask_questions(self):
        
        if not self.questions:
            raise ValueError('No questions have been generated')
            
        for q in self.questions:
            question = {
                'type': 'input',
                'name': q['question_string'],
                'message': q['question_string'],
                'validate': lambda val: val.isdigit() or 'Please enter an integer'
                }
            
            response = prompt(question, style=self.style)
            user_answer = response[q['question_string']]
            correct = int(user_answer) == q['answer']
            
            answer_dict = dict(question_string=q['question_string'],
                               user_answer=user_answer,
                               answer=q['answer'],
                               correct=correct)
            self.answers.append(answer_dict)
            
    def calculate_score(self):
        
        if not self.answers:
            raise ValueError('No answers have been generated')
            
        incorrect_answers = len([i for i in self.answers if not i['correct']])
        
        self.score = (1 - incorrect_answers / len(self.answers)) * 100   

    def display_output(self):
        if self.score >= 70:
            output = f"\nCongratulations!\nYou scored {self.score}%!\n"
        else:
            output = f"\nBad news!\nYou scored {self.score}% ... better luck next time.\n"
        
        print(output)
        
    def reset_answers(self):
        self.answers = []
        
    def reset_questions(self):
        self.questions = []
        
    def prompt_proceed(self):
                
        proceed_question = {
            'type': 'list',
            'name': 'proceed_selection',
            'message': 'How would you like to proceed?',
            'choices': [{'name': op} for op in self.proceed_options]
        }
        
        proceed_response = prompt(proceed_question, style=self.style)
        self.selected_proceed = proceed_response['proceed_selection']
        
    
if __name__ == "__main__": 
    
    operators = ['addition', 'multiplication', 'subtraction', 'division']
    math_test = MathTest(operators=operators, test_length=2)    
    
    while math_test.selected_proceed != 'quit':
        
        if not math_test.selected_proceed:
            math_test.prompt_operator()
            math_test.generate_questions()
            math_test.ask_questions()
            math_test.calculate_score()    
            math_test.display_output()   
            math_test.prompt_proceed()    
        
        elif math_test.selected_proceed == 'retry':
            math_test.reset_answers()
            math_test.ask_questions()
            math_test.calculate_score() 
            math_test.display_output() 
            math_test.prompt_proceed()
            
        elif math_test.selected_proceed == 'new test':
            math_test.reset_answers()     
            math_test.reset_questions()
            math_test.prompt_operator()
            math_test.generate_questions()
            math_test.ask_questions()
            math_test.calculate_score()    
            math_test.display_output()   
            math_test.prompt_proceed() 
            
        else:
            # this should never occur, it is a fail-safe
            quit()
    
    quit()
            
    
        
    
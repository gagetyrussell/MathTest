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

from PyInquirer import style_from_dict, Token, prompt, Separator
from pprint import pprint
from random import randint

class MathTest():
        
    def __init__(self, operators: list, test_length=10) -> str:
        """
        A MathTest CLI Program

        Parameters
        ----------
        operators : list
            A list of arithmetic operators.
            supports: addition, multiplication, subtraction, division
        test_length : int, optional
            The number of questions to be asked. The default is 10.

        Raises
        ------
        ValueError
            If an unsupported operator is used.

        """
        
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
        """
        Asks the user what they would like to be tested on

        Returns
        -------
        str
            The selected operator.

        """
        
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
        """
        Generate random numbers for questions based on operator:
            The criteria is:
                answer is a positive integer
                
                for division, this means we can use prime numbers
                for subtraction this means that second_number < first_number

        Raises
        ------
        ValueError
            If an unsupported operator is used. This should never be reached as it is caught in init.

        Returns
        -------
        numbers : tuple
            the first and second number to be used in the question. Both TYPE int.
        """
        if self.selected_operator == 'division':
            # we cannot have a prime number
            first_number = get_random_nonprime(2,100)
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
            # this line should never be hit. It is a fail-safe.
            raise ValueError('Unsupported Operators')
            
        return (first_number, second_number)
    
    def generate_question(self):
        """
        Generate the question object. The question object is a dict with a question_string and an answer.

        Returns
        -------
        question_dict : dict
            A dict with the question string and evaluated answer.

        """
        number = self.get_numbers()
        question_string = f"{number[0]} {self.supported_operators[self.selected_operator]} {number[1]}"
        answer = eval(question_string)
        
        question_dict = dict(question_string=question_string, answer=answer)
        
        return question_dict
            
    def generate_questions(self):
        """
        Generate list of questions to be tested

        Returns
        -------
        list
            The question objects to be used for testing.

        """

        for i in range(self.test_length):
            self.questions.append(self.generate_question())
            
        return self.questions
            
    def ask_questions(self):
        """
        Prompt the user to answer the questions.

        Raises
        ------
        ValueError
            If no questions have been generated.

        Returns
        -------
        None.

        """
        
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
        """
        Calculate the test score.

        Raises
        ------
        ValueError
            If questions have not been answered.

        Returns
        -------
        None.

        """
        
        if not self.answers:
            raise ValueError('No answers have been generated')
            
        incorrect_answers = len([i for i in self.answers if not i['correct']])
        
        self.score = (1 - incorrect_answers / len(self.answers)) * 100   

    def display_output(self):
        """
        Display the users score and pass/fail

        Returns
        -------
        None.

        """
        if self.score >= 70:
            output = f"\nCongratulations!\nYou scored {round(self.score, 1)}%!\n"
        else:
            output = f"\nBad news!\nYou scored {round(self.score, 1)}% ... better luck next time.\n"
        
        print(output)
        
    def reset_answers(self):
        """
        Reset answers if user wants to retry the same test.

        Returns
        -------
        None.

        """
        self.answers = []
        
    def reset_questions(self):
        """
        Reset questions if user wants a new test.

        Returns
        -------
        None.

        """
        self.questions = []
        
    def prompt_proceed(self):
        """
        Ask the user how they would like to proceed after completing a test.

        Returns
        -------
        None.

        """
                
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
    math_test = MathTest(operators=operators, test_length=10)    
    
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
            
    
        
    
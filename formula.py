# class to represent a formula for finding the roots of a n-th degree polynomial.
import numpy as np
import copy
import unittest
import random

def pretty_print_formula(formula):
    """
    Takes in a list-form formula and makes a slightly more readable form of
    the actual computed formula. (Work back from final index)

    formula : List
        List matching Formula's formula field format.
    """
    def print_unit(formula_unit):
        """
        Helper function, will recursively print the formula element
        
        formula_unit : Tuple
            Either an operation tuple, a constant, or a coefficient.
            
        print_string : str
            The string representing the actual formula  
        """
        if type(formula_unit) is tuple:
            # Split formula unit into operation, atomic1, atomic2
            op, at1, at2 = formula_unit
            
            if op == "root":
                op = " root "
            
            print_string ='('
            
            
            print_string += print_unit(formula[at1])
            print_string += op
            print_string += print_unit(formula[at2])
            
            print_string += ')'
            return print_string
        else:
            # Its only an atomic, convert to string
            return str(formula_unit)
    print("\n",print_unit(formula[-1]),"\n")
    

class Formula:
    """
    Formula class
    Represents a mathematical formula to find a root of a polynomial (i.e the Quadratic Formula)

    """
    OPERATIONS = ['+', '-', '*', '/', '**','root']
    CONSTANTS = [(1),(2),(3),(4)]
    #options for equation coefficients
    FIRST_DEGREE = [('a'), ('b')]
    SECOND_DEGREE = [('a'),('b'),('c')]

    def __init__(self,min_length, max_length, degree_of_polynomial):
        self.max_length = max_length
        self.min_length = min_length
        self.degree_of_polynomial = degree_of_polynomial
        self.formula = []
        self.length_of_constants = -1

        #determine which coefficent set to use for formula
        if self.degree_of_polynomial == 1:
            self.formula.extend(self.FIRST_DEGREE)  # add appropriate coefficients to the formula linked list
            self.formula.extend(self.CONSTANTS)  # add constants to the formula
            self.length_of_constants = len(self.FIRST_DEGREE) + len(self.CONSTANTS)

        if self.degree_of_polynomial == 2:
            self.formula.extend(self.SECOND_DEGREE) # add appropriate coefficients to the formula linked list
            self.formula.extend(self.CONSTANTS) # add constants to the formula
            self.length_of_constants = len(self.SECOND_DEGREE) + len(self.CONSTANTS)

        #randomly generate a formula in of random length in specified range
        for _ in range(random.choice(range(self.min_length,self.max_length))):
            operator = random.choice(self.OPERATIONS) #randomly choose operator to be added
            first_pointer, second_pointer = random.sample(range(len(self.formula)), 2) #pick two random new elements to point to
            self.formula.append((operator, first_pointer, second_pointer))

    def evaluate_formula(self, expression):
        a, b, c, root_1, root_2 = expression
        constants = self.formula[self.length_of_constants:]


        #replace variables with actual values
        for j in range(len(constants)):
            if constants[j] == 'a':
                self.formula[j] = a
            if constants[j] == 'b':
                self.formula[j] = b
            if constants[j] == 'c':
                self.formula[j] = c

        values = self.formula[:self.length_of_constants]
        for i in range(self.length_of_constants,len(self.formula)):
            operator, first_pointer, second_pointer = self.formula[i]
            first_pointer = int(first_pointer)
            second_pointer = int(second_pointer)


            # check the pointers refer to valid indices
            if first_pointer < len(values) and second_pointer < len(values):
                left_value = values[first_pointer]
                right_value = values[second_pointer]

                result = None

                if operator == '+':
                    result = left_value + right_value
                if operator == '-':
                    result = left_value - right_value
                if operator == '*':
                    result = left_value*right_value
                if operator == '/':
                    result = left_value / right_value
                if operator == '**':
                    result = left_value ** right_value
                if operator == 'root':
                    result = left_value ** (1/right_value)

                # check if result is none
                if result is not None:
                    values.append(result)
        return values[-1]


if __name__ == '__main__':
    formula = Formula(5,20,2)
    print(formula.formula)
    pretty_print_formula(formula.formula)
    # formula.evaluate_formula((1,1,1,1,1))










# class to represent a formula for finding the roots of a n-th degree polynomial.
import numpy as np
import copy
import unittest
import random
class Formula:
    """
    Formula class
    Represents a mathematical formula to find a root of a polynomial (i.e the Quadratic Formula)

    """
    OPERATIONS = ['+', '-', '*', '/', '**']
    CONSTANTS = [(1),(2),(3),(4)]
    #options for equation coefficients
    FIRST_DEGREE = [('a'), ('b')]
    SECOND_DEGREE = [('a'),('b'),('c')]

    def __init__(self,min_length, max_length, degree_of_polynomial):
        self.max_length = max_length
        self.min_length = min_length
        self.degree_of_polynomial = degree_of_polynomial
        self.formula = []

        #determine which coefficent set to use for formula
        if self.degree_of_polynomial == 1:
            self.formula.extend(self.FIRST_DEGREE)  # add appropriate coefficients to the formula linked list
            self.formula.extend(self.CONSTANTS)  # add constants to the formula

            #self.coefficient_options = self.FIRST_DEGREE
        if self.degree_of_polynomial == 2:
            self.formula.extend(self.SECOND_DEGREE) # add appropriate coefficients to the formula linked list
            self.formula.extend(self.CONSTANTS) # add constants to the formula

        #randomly generate a formula in of random length in specified range
        for _ in range(random.choice(range(self.min_length,self.max_length))):
            operator = random.choice(self.OPERATIONS) #randomly choose operator to be added
            first_pointer, second_pointer = random.sample(range(len(self.formula)), 2) #pick two random new elements to point to
            self.formula.append((operator, first_pointer, second_pointer))



        def solve_quadratic_equation(self, a, b, c, root_1, root_2):
            """
            Calculate the roots of a quadratic polynomial with coefficients a,b,c.
            Returns the calculated root and the percent error to the actual closest root.
            """
        def solve_linear_equation(self, m, b ,y, answer_x):
            """
            Calculate the value of x to satisfy a linear equation in standard form with coefficients m, b, y
            Returns the calculated root and percent error to the actual root.
            """

        def fitness_function(self):
            """
            Calculate the fitness of the polynomial by solving the equations in the dataset
            Returns the average percent error of all the solutions.
            """
            pass






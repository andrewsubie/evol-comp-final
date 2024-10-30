# class to represent a formula for finding the roots of a n-th degree polynomial.
import random

class Formula:
    """
    Formula class
    Represents a mathematical formula to find a root of a polynomial (i.e., the Quadratic Formula).
    """
    # string representation of mathematical operators
    OPERATIONS = ['+', '-', '*', '/', '**', 'root']
    # options for constants in formula
    CONSTANTS = [1, 2, 3, 4]
    # options for equation coefficients
    FIRST_DEGREE = ['a', 'b']
    SECOND_DEGREE = ['a', 'b', 'c']

    def __init__(self, min_length, max_length, degree_of_polynomial):
        """
        Constructor takes arguments to specify length of formula, degree of polynomial that it is intended to solve for the roots of
        to load the appropriate constants into the formula
        @param: min_length, max_length, degree_of_polynomial
        @return: None
        """
        self.max_length = max_length
        self.min_length = min_length
        self.degree_of_polynomial = degree_of_polynomial
        self.formula = []
        self.length_of_constants = -1

        # determine which coefficient set to use for formula based on the degree of polynomial the formula is intended to solve
        # add apppropriate coeff. set and constants to the formula
        if self.degree_of_polynomial == 1:
            self.formula.extend(self.FIRST_DEGREE)
            self.formula.extend(self.CONSTANTS)
            self.length_of_constants = len(self.FIRST_DEGREE) + len(self.CONSTANTS)

        elif self.degree_of_polynomial == 2:
            self.formula.extend(self.SECOND_DEGREE)
            self.formula.extend(self.CONSTANTS)
            self.length_of_constants = len(self.SECOND_DEGREE) + len(self.CONSTANTS)

        # randomly generate a formula of length within allowed range
        for _ in range(random.randint(self.min_length, self.max_length)):
            operator = random.choice(self.OPERATIONS)  #choose operator
            first_pointer, second_pointer = random.sample(range(len(self.formula)), 2)  # pick two random elements to point to
            self.formula.append((operator, first_pointer, second_pointer))

    def evaluate_formula_quadratic(self, expression):
        """
        Evaluates the formula by iterating through self.formula for a given expression, replacing the
        coefficient variables in self.formula with actual values and returns the calculated root
        @param: expression (5-tuple to represent the three coefficients and two roots of a quadratic equation in
        standard form, expected in order (a, b, c, root_1, root_2) for ax2+bx+c with roots root_1, root_2)
        @return: calulcated root (float value)
        """
        a, b, c, root_1, root_2 = expression
        constants = self.formula[:self.length_of_constants] #isolate constants

        # replace variables with actual values
        for j in range(len(constants)):
            if constants[j] == 'a':
                constants[j] = a
            elif constants[j] == 'b':
                constants[j] = b
            elif constants[j] == 'c':
                constants[j] = c

        values = list(constants)  # list of actual values
        #perform each operation specified in the length of the formula
        for i in range(self.length_of_constants, len(self.formula)):
            operator, first_pointer, second_pointer = self.formula[i]
            # check iff pointers return actual values
            if first_pointer < len(values) and second_pointer < len(values):
                left_value = values[first_pointer]
                right_value = values[second_pointer]

                result = None #init result
                try:
                    if operator == '+':
                        result = left_value + right_value
                    elif operator == '-':
                        result = left_value - right_value
                    elif operator == '*':
                        result = left_value * right_value
                    elif operator == '/':
                        if right_value != 0: # handle 0 division
                            result = left_value / right_value
                        else:
                            pass
                    elif operator == '**':
                        if right_value >= 0 and left_value != 0: #handle negative exponentiation
                            result = left_value ** right_value
                        else:
                            pass
                    elif operator == 'root':
                        if right_value != 0 and left_value > 0: #handle 0 root
                            result = left_value ** (1 / right_value)
                        else:
                            pass
                except Exception as e:
                    print(e)
                    values.append(values[-1])

                # append result of ea. operation to values
                if isinstance(result, int) or isinstance(result, float):
                    values.append(result)
        # return last calculated value (root) or None if none is calculated
        if values:
            return values[-1]
        else:
            return None

if __name__ == '__main__':
    TEST_CASES = 50
    MIN_LENGTH = 5
    MAX_LENGTH = 20
    # quadratic test case
    expression_1 = (1,2,1,-1,-1)
    expression_2 = (1,7,6,-1.0,-6.0)
    expression_3 = (1,-41,288,-9.0,-32.0)
    results = []
    for _ in range(TEST_CASES):
        f = Formula(MIN_LENGTH, MAX_LENGTH, 2)
        r1 = f.evaluate_formula_quadratic(expression_1)
        r2 = f.evaluate_formula_quadratic(expression_2)
        r3 = f.evaluate_formula_quadratic(expression_3)
        print(r1, r2, r3)
        results.append(r1)
        results.append(r2)
        results.append(r3)
    for result in results:
        assert(result is not None)
        assert(isinstance(result,int) or isinstance(result,float))











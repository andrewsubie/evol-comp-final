# class to represent a formula for finding the roots of a n-th degree polynomial.
import random
import copy
import csv
import numpy as np

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
    FIRST_DEGREE = ['m', 'b', 'y']
    SECOND_DEGREE = ['a', 'b', 'c']

    def __init__(self, min_length, max_length, degree_of_polynomial, path_to_data):
        """
        Constructor takes arguments to specify length of formula, degree of polynomial that it is intended to solve for the roots of
        to load the appropriate constants into the formula.
        Path to data is assuemed to be a CSV full of various equations
        @param: min_length, max_length, degree_of_polynomial, path to data
        @return: None
        """
        self.fitness = None
        # init fitness
        self.path_to_data = path_to_data
        self.max_length = max_length
        self.min_length = min_length
        self.degree_of_polynomial = degree_of_polynomial
        self.formula = []
        self.length_of_constants = -1
        self.data = []
        # data to evaluate formula on
        with open(path_to_data, newline='', encoding='utf-8') as csvfile:
            csv_reader = csv.reader(csvfile,delimiter=',')
            for i, row in enumerate(csv_reader):
                if i > 1:
                    self.data.append(row)
                if i == 10:
                    break


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
            
            # This is a bit of an extreme fix, however it works to
            # prevent absurdly large numbers
            # Only allow constants to act as second operator in exponent situations
            if operator == '**' or operator == 'root':
                second_pointer = np.random.randint(self.degree_of_polynomial+2, self.length_of_constants)
            
            self.formula.append((operator, first_pointer, second_pointer))

    def extend_formula(self):
        """
        Extend the formula by another operator if it is below the max_length
        """
        if len(self.formula) < self.max_length:
            operator = random.choice(self.OPERATIONS)
            first_pointer, second_pointer = random.sample(range(len(self.formula)), 2)
            self.formula.append((operator, first_pointer, second_pointer))
        else:
            print(f'Formula is already at max length: {self.max_length}')


    def mutate_formula(self,num_elements_to_mutate):
        """
        For the number of elements specified in num_elements_to_mutate, a randomly selected element is selected and changed
        to a new value.
        @param elements_to_mutate: specifies number of elements to mutate
        @return None
        """
        # select indices to mutate
        indices_to_mutate = random.sample(range(self.length_of_constants, len(self.formula)), num_elements_to_mutate)
        # generate new block in formula
        for index in indices_to_mutate:
            # Change here: Must constrict to only pointing backwards!
            operator = random.choice(self.OPERATIONS)
            first_pointer, second_pointer = random.sample(range(index), 2)
            
            # Only allow constants to act as second operator in exponent situations
            if operator == '**' or operator == 'root':
                second_pointer = np.random.randint(self.degree_of_polynomial+2, self.length_of_constants)
            
            self.formula[index] = (operator, first_pointer, second_pointer)

    def eval_fitness(self):
        """
        Evaluates the formula for each data in the test data set, calculates the error for the closest root
        and returns the mean error of the test dataset.
        Updates self.fitness
        :return: self.fitness
        """
        def pct_error(orig, priv):
            """
            Inner-wrapper function to calculate percent error
            """
            return np.abs(orig - priv) / orig * 100.0

        errors = []
        if self.degree_of_polynomial == 1:
            for row in self.data:
                m, x, b, y = row
                expression = (m, b, y)
                calc_result = self.evaluate_formula(expression)
                errors.append(pct_error(x, calc_result))
        if self.degree_of_polynomial == 2:
            for row in self.data:
                id, path, a, b, c, root_1, root_2, equation = row
                expression = (float(a), float(b), float(c), float(root_1), float(root_2))
                print(expression)
                calc_result = self.evaluate_formula(expression)
                row_errors = []
                row_errors.append(pct_error(float(root_1), calc_result))
                row_errors.append(pct_error(float(root_2), calc_result))
                errors.append(np.min(row_errors))
        # calculate mean error and convert to logarithmic scale to accomodate large errors, higher fitness = less error (intuition)
        mean_error = np.abs(np.mean(errors))
        self.fitness =  100 / (1 + np.log(mean_error + 1))
        return self.fitness, mean_error



    def pretty_print_formula(self):
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
                print_string = '('

                print_string += print_unit(self.formula[at1])
                print_string += op
                print_string += print_unit(self.formula[at2])

                print_string += ')'
                return print_string
            else:
                # Its only an atomic, convert to string
                return str(formula_unit)

        print("\n", print_unit(self.formula[-1]), "\n")
        print_unit(self.formula[-1]),

    def evaluate_formula(self, expression):
        """
        Evaluates the formula by iterating through self.formula for a given expression, replacing the
        coefficient variables in self.formula with actual values and returns the calculated root
        @param: expression (5-tuple to represent the three coefficients and two roots of a quadratic equation in
        standard form, expected in order (a, b, c, root_1, root_2) for ax2+bx+c with roots root_1, root_2)
        @return: calulcated root (float value)
        """
        if self.degree_of_polynomial == 1:
            m, root_1, b, y = expression
            constants = self.formula[:self.length_of_constants]
            for j in range(len(constants)):
                if constants[j] == 'm':
                    constants[j] = m
                if constants[j] == 'b':
                    constants[j] = b
                if constants[j] == 'y':
                    constants[j] = y

        if self.degree_of_polynomial == 2:
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

def crossover_formulas(parent_a, parent_b, len_consts = 7, crossover_points = 2):
    """
    Combines two formula genotypes (<formula_name>.formula) into X children

    parent_a, formula_b : Lists
        Lists matching Formula's formula field format.
    """
    # For ease of writing, the maximum crossover point MUST be less than the shortest length
    # otherwise it would be possible to shift the formula-elements down a few indices,
    # which would introduce the chance for a cyclic reference, which would be bad
    min_length = min(len(parent_a), len(parent_b))
    
    # Pick two indices to select between
    # Min should be the length of constants, as those should be the same
    # for both parents -- it would be wasteful to crossover there
    # The min_length+1 allows for a pseudo-1-pt crossover, should the max be the biggest value
    crossover_points = np.sort(np.random.randint(len_consts,
                                                 min_length+1,
                                                 crossover_points))
    
    point_a = crossover_points[0]
    
    child_a = parent_a[0:point_a]
    child_b = parent_b[0:point_a]
    
    parents = (parent_a, parent_b)
    p_select = 1
    # If the two points match, then it will be like pure inheritance
    for cross_point in crossover_points[1:]:
        point_b = cross_point
        
        child_a.extend(parents[p_select][point_a:point_b])
        child_b.extend(parents[1 - p_select][point_a:point_b])
            
        # Swap primary and secondary parents
        p_select = 1 - p_select
            
        # Set point a to the old cross point
        point_a = cross_point

    child_a.extend(parents[p_select][point_a:])
    child_b.extend(parents[1 - p_select][point_a:])
    
    return child_a, child_b

if __name__ == '__main__':
    TEST_CASES = 50
    MIN_LENGTH = 5
    MAX_LENGTH = 20
    #file paths
    PATH_TO_LINEAR = './data/linear_equations_1_variable.csv'
    PATH_TO_QUAD = './data/quadratic_equation_full_details.csv'
    """
    test printing
    """
    print("PRINTING TEST RESULTS")
    f_test = Formula(5, 20, 2,PATH_TO_QUAD)
    f_test.pretty_print_formula()
    """
    linear test case
    """
    print("LINEAR")
    linear_expression = (-6,-4,-93,-69)

    for _ in range(TEST_CASES):
        f_linear = Formula(MIN_LENGTH, MAX_LENGTH, 1,PATH_TO_LINEAR)
        f_linear.pretty_print_formula()
        r1 = f_linear.evaluate_formula(linear_expression)
        print(r1)

    """
    quadratic test case
    """
    print("QUADRATIC")
    expression_1 = (1,2,1,-1,-1)
    expression_2 = (1,7,6,-1.0,-6.0)
    expression_3 = (1,-41,288,-9.0,-32.0)
    results = []
    for _ in range(TEST_CASES):
        f = Formula(MIN_LENGTH, MAX_LENGTH, 2, PATH_TO_QUAD)
        r1 = f.evaluate_formula(expression_1)
        r2 = f.evaluate_formula(expression_2)
        r3 = f.evaluate_formula(expression_3)
        print(r1, r2, r3)
        results.append(r1)
        results.append(r2)
        results.append(r3)
    for result in results:
        assert(result is not None)
        assert(isinstance(result,int) or isinstance(result,float))
    print("Fitness" + str(f_test.eval_fitness()))
    """
    mutation test case
    """
    print("\nTest Mutation")
    try:
        f_mut = Formula(MIN_LENGTH, MAX_LENGTH, 2, PATH_TO_QUAD)
        print("Pre-mutation")
        print(f_mut.formula)
        f_mut.pretty_print_formula()
        print("Post-mutation")
        f_mut.mutate_formula(3)
        print(f_mut.formula)
        f_mut.pretty_print_formula()
    except RecursionError:
        print("Mutation caused problem")
    
    """
    crossover test case
    """
    print("\nTest Crossover")
    try:
        pf_a = Formula(MIN_LENGTH, MAX_LENGTH, 2, PATH_TO_QUAD)
        pf_b = Formula(MIN_LENGTH, MAX_LENGTH, 2, PATH_TO_QUAD)
        
        child_a = copy.deepcopy(pf_a)
        child_a.fitness = None
        child_b = copy.deepcopy(pf_b)
        child_b.fitness = None
        
        print("Pre-crossover")
        
        print(f"Parent A: {pf_a.formula}")
        pf_a.pretty_print_formula()
        print(f"Parent B: {pf_b.formula}")
        pf_b.pretty_print_formula()
        
        print('Post-crossover')
        child_a.formula, child_b.formula = crossover_formulas(pf_a.formula, pf_b.formula, pf_a.length_of_constants)
        print(f"Child A: {child_a.formula}")
        child_a.pretty_print_formula()
        print(f"Child B: {child_b.formula}")
        child_b.pretty_print_formula()
        
    except Exception as e:
        print(e,'Crossover caused problem')









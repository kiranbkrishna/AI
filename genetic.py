# Author: Kiran Balakrishnan
2# Geneteic algorithm trial to generate a target number
# More on problem defenition @ http://www.ai-junkie.com/ga/intro/gat3.html
from random import Random
operators_numbers = dict([(str(i), bin(i).replace('0b','').zfill(4) ) for i in range(10)])
opertions = ['+', '-', '*', '/']
operators_functions = {}
operators_functions['+'] = '1010'
operators_functions['-'] = '1011'
operators_functions['/'] = '1100'
operators_functions['*'] = '1101'
population_limit = 10
DEBUG = True
TARGET = 25

class SolutionArrived(Exception):
    pass

def decode_individual(individual):
    to_string = []
    for i in individual:
        values = operators_numbers.values()
        keys = operators_numbers.keys()
        if i in values:
            to_string.append(keys[values.index(i)])

        values = operators_functions.values()
        keys = operators_functions.keys()
        if i in values:
            to_string.append(keys[values.index(i)])
    ret = '\t'.join(to_string)
    # if DEBUG:
    #     print ret
    return ret

def add_to_population(individual, generation):
    if not population_matrix.get(generation):
        population_matrix[generation] = [individual]
    else:
        population_matrix[generation].append(individual)

def create_chromosomes(chromosome_length):
    assert type(chromosome_length) == int
    r = Random()
    operations_length = len(opertions)
    return [operators_numbers[str(r.randint(0, 9))] if not i%2 else operators_functions[opertions[r.randint(0, operations_length - 1)]] for i in range(chromosome_length)]

def see_population(generation):
    for i in population_matrix[generation]:
        decode_individual(i)

def evaluate_individual(individual):
    stack = []
    print "evaluating --- ", individual
    print decode_individual(individual)
    individual.reverse()
    s = decode_individual(individual)
    for i in s.split('\t'):
        stack.append(i)
    result = None
    is_first_time = True
    while stack:
        if is_first_time:
            operand1 = stack.pop()
            is_first_time = False
        else:
            operand1 = result
        operation = stack.pop()
        operand2 = stack.pop()
        try:
            if DEBUG:
                print "Evaluating" +  str(operand1) + ' ' + operation + ' ' + str(operand2)
            result = eval(str(operand1) + ' ' + operation + ' ' + str(operand2))
        except ZeroDivisionError, e:
            if not result:
                result = 0
    if DEBUG:
        print result
    return result

def fitness(individual):
    value = evaluate_individual(individual)
    diff = TARGET - value
    if not diff:
        raise SolutionArrived("Viola we have reached the solution")
    return abs(diff)

if __name__ == '__main__':
    generation = 0
    population_matrix = {}
    chromosome_length = 7
    # creating initial population
    for i in range(population_limit):
        chromosome = create_chromosomes(chromosome_length)
        add_to_population(chromosome, generation)
    print "current generation ", generation
    print population_matrix
    see_population(generation)
    current_population_fitness = {}
    for chromosome in population_matrix[generation]:
        cr = decode_individual(chromosome)
        current_population_fitness[cr] = (fitness(chromosome), chromosome)
        # print chromosome
        # print cr
        # print current_population_fitness[cr], "\n\n"
    for key, value in current_population_fitness.items():
        print key + " ------> " , value
    keys_sorted = sorted(current_population_fitness, key=lambda(x):current_population_fitness[x][0])

    print "evaluation result "
    for k in keys_sorted[:len(keys_sorted)/2]:
        print k + " -----> ", current_population_fitness[k]
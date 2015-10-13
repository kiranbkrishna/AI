# Author: Kiran Balakrishnan
# Geneteic algorithm trial to generate a target number
# More on problem defenition @ http://www.ai-junkie.com/ga/intro/gat3.html
from random import Random
import re
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
crossover_lesion_count = 3

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

def get_next_operation(stack):
    try:
        operation = stack.pop()
        while not is_operation(operation):
            operation = stack.pop()
        return operation
    except Exception, e:
        return None

def get_next_operand(stack):
    try:
        operand1 = stack.pop()
        while not is_operand(operand1):
            operand1 = stack.pop()
        return operand1
    except Exception, e:
        return None


def evaluate_individual(individual):
    stack = []
    if DEBUG:
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
            operand1 = get_next_operand(stack)
            is_first_time = False
        else:
            operand1 = result
        operation = get_next_operation(stack)
        operand2 = get_next_operand(stack)
        if operand1 == None or operation == None or operand2 == None:
            break
        else:
            try:
                # if DEBUG:
                #     print "Evaluating" +  str(operand1) + ' ' + operation + ' ' + str(operand2)
                result = eval(str(operand1) + ' ' + operation + ' ' + str(operand2))
            except ZeroDivisionError, e:
                if not result:
                    result = int(operand1)
    if DEBUG:
        print result
    return result

def is_operation(i):
    return i in ['+', '-', '*', '/']

def is_operand(i):
    try:
        return int (i) in [0, 1, 2, 3, 4, 5, 6, 7, 8, 9]
    except Exception, e:
        return False

def create_offsprings(chromosome1, chromosome2):
    p1 = ''.join(chromosome1)
    p2 = ''.join(chromosome2)
    r =  Random()
    length = len(p1)
    break_at = r.randint(1, length - 1)
    c1 = p1[:break_at] + p2[break_at:]
    c2 = p1[break_at:] + p2[:break_at]
    return re.findall( '\d{4}', c1), re.findall( '\d{4}', c2)

def fitness(individual):
    value = evaluate_individual(individual)
    if not value:
        value = 0
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
    while True:
        print "current generation ", generation
        print population_matrix[generation]
        see_population(generation)
        current_population_fitness = {}
        for chromosome in population_matrix[generation]:
            individual = chromosome
            cr = decode_individual(individual)
            try:
                current_population_fitness[cr] = (fitness(individual), chromosome)
            except SolutionArrived as e:
                print "Target value achied by " + cr
        if DEBUG:
            for key, value in current_population_fitness.items():
                print key + " ------> " , value
        keys_sorted = sorted(current_population_fitness, key=lambda(x):current_population_fitness[x][0])
        if DEBUG:
            print "evaluation result"
        selected_chromosomes = []
        for k in keys_sorted[:len(keys_sorted)/2]:
            # if DEBUG:
            print k + " -----> ", current_population_fitness[k]
            selected_chromosomes.append(current_population_fitness[k][1])
        print "selected_chromosomes ", selected_chromosomes
        generation += 1
        length = len(selected_chromosomes)
        r = Random()
        count = population_limit
        print 'creating next generation'
        while count:
            parent_1 = selected_chromosomes[r.randint(0, length - 1)]
            parent_2 = selected_chromosomes[r.randint(0, length - 1)]
            (c1, c2) = create_offsprings(parent_1, parent_2)
            add_to_population(c1, generation)
            add_to_population(c2, generation)
            count -= 2

import random
import pandas


def read_data():
    """Reads data from csv file and returns tuple."""
    data = pandas.read_csv("zbior_danych_ag.csv", delimiter=';')

    weights_return = []
    values_return = []
    capacities_return = []

    for _, row in data.iterrows():
        weights_row = list(map(int, row['Ciezar'][1:-1].split()))
        values_row = list(map(int, row['Ceny'][1:-1].split()))
        capacity_row = int(row['Pojemnosc'])

        weights_return.append(weights_row)
        values_return.append(values_row)
        capacities_return.append(capacity_row)

    return weights_return, values_return, capacities_return


def print_row(row_number: int):
    """Prints row of knapsack problem data."""
    print("ciężary:", weights_list[row_number])
    print("ceny:", values_list[row_number])
    print("pojemność:", capacities_list[row_number])


def generate_starting_population(population_size: int):
    """Generates starting population of random chromosomes."""
    population_return = []
    for _ in range(population_size):
        chromosome = []
        for _ in range(5):
            chromosome.append(random.randint(0, 1))
        population_return.append(chromosome)
    return population_return


def fitness(chromosome: list[int], weights: list[int], values: list[int], capacity: int):
    """Returns fitness value of given chromosome."""
    total_weight = 0
    total_value = 0

    for i, gene in enumerate(chromosome):
        if gene == 1:
            total_weight += weights[i]
            total_value += values[i]

    if total_weight > capacity:
        total_value = total_value - (2 * (total_weight-capacity))

    # if total_value < 0:
    #    total_value = 0
    return total_value


def print_chromosome(chromosome: list[int], weights: list[int], values: list[int]):
    """Prints chromosome with its weights and values added."""
    print("chromosom:", chromosome)

    weight_calculation = "ciężar: "
    value_calculation = "cena: "
    total_weight = 0
    total_value = 0

    for i, gene in enumerate(chromosome):
        if gene == 1:
            weight_calculation += str(weights[i]) + " + "
            value_calculation += str(values[i]) + " + "
            total_weight += weights[i]
            total_value += values[i]
    weight_calculation += " = "+str(total_weight)
    value_calculation += " = "+str(total_value)
    print(weight_calculation)
    print(value_calculation)


weights_list, values_list, capacities_list = read_data()


row_number = 200
print_row(row_number)
weights = weights_list[row_number]
values = values_list[row_number]
capacity = capacities_list[row_number]
population = generate_starting_population(10)


print(population)
print(weights)
print(values)
print(capacity)

for _, chromosome in enumerate(population):
    print_chromosome(chromosome, weights, values)
    print("fitness", fitness(chromosome, weights, values, capacity), "\n")

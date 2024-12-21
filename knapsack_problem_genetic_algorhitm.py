import random
import pandas


def read_data():
    """Reads data from csv file and returns tuple."""
    data = pandas.read_csv("zbior_danych_ag.csv", delimiter=';')

    weights_list = []
    values_list = []
    capacities_list = []

    for index, row in data.iterrows():
        weights_row = list(map(int, row['Ciezar'][1:-1].split()))
        values_row = list(map(int, row['Ceny'][1:-1].split()))
        capacity_row = int(row['Pojemnosc'])

        weights_list.append(weights_row)
        values_list.append(values_row)
        capacities_list.append(capacity_row)

    return weights_list, values_list, capacities_list


def print_row(row_number: int):
    print("ciężary:", weights[row_number])
    print("ceny:", values[row_number])
    print("pojemność:", capacities[row_number])


def generate_starting_population():
    """Generates starting population of random chromosomes."""
    population_return = []
    for _ in range(10):
        chromosome = []
        for _ in range(5):
            chromosome.append(random.randint(0, 1))
        population_return.append(chromosome)
    return population_return


weights, values, capacities = read_data()

print_row(0)

population = generate_starting_population()

print(population)

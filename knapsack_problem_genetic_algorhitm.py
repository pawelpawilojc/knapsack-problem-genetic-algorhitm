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


def crossover_1(father: list[int], mother: list[int], point: int):
    """One-point crossover function returning tuple two children (list[int])"""
    offspring_1 = father[:point] + mother[point:]
    offspring_2 = mother[:point] + father[point:]
    return offspring_1, offspring_2


test_1, test_2 = crossover_1(population[0], population[1], 3)
print("offspring_1:")
print_chromosome(test_1, weights, values)
print("offspring_2")
print_chromosome(test_2, weights, values)


def crossover_2(father: list[int], mother: list[int], point_1: int, point_2: int):
    """Two-point crossover function returning tuple two children (list[int])"""
    offspring_1 = (father[:point_1] +
                   mother[point_1:point_2] + father[point_2:])
    offspring_2 = (mother[:point_1] +
                   father[point_1:point_2] + mother[point_2:])
    return offspring_1, offspring_2


test_1, test_2 = crossover_2(population[0], population[1], 2, 4)
print("offspring_1:")
print_chromosome(test_1, weights, values)
print("offspring_2:")
print_chromosome(test_2, weights, values)


# lista 3
# 2. Opracować algorytm selekcji turniejowej:
# a. Zaimplementować proces losowego wyboru osobników do turniejów.
# b. Zaprojektować mechanizm wyboru najlepszego osobnika z każdego turnieju.
def tournament_selection(population, weights, values, capacity):
    """Tournament selection returning winners - half of the population"""
    tournament_winners = []
    while (len(population) > 0):
        chromosome_1 = random.choice(population)
        population.remove(chromosome_1)
        chromosome_2 = random.choice(population)
        population.remove(chromosome_2)
        if fitness(chromosome_1, weights, values, capacity) > fitness(chromosome_2, weights, values, capacity):
            tournament_winners.append(chromosome_1)
        else:
            tournament_winners.append(chromosome_2)
    return tournament_winners

# 3. Opracować algorytm selekcji proporcjonalnej (metoda ruletki):
# a. Obliczyć prawdopodobieństwa selekcji na podstawie wartości funkcji
# przystosowania.
# b. Zaimplementować mechanizm wyboru osobników na podstawie tych
# prawdopodobieństw.


def roulette_selection(population, weights, values, capacity):
    """Roulette selection returning only one parent"""
    roulette_population = []
    for _, chromosome in enumerate(population):
        counter = 0
        while counter < fitness(chromosome, weights, values, capacity):
            roulette_population.append(chromosome)
            counter += 1
    return random.choice(roulette_population)

# 4. Zaprojektować operator mutacji punktowej:
# a. Określić mechanizm losowego wyboru genów do mutacji.
# b. Zdefiniować zmiany w wybranym genie zgodnie z założeniami problemu


def mutation(population, percent: int):
    """Mutation of population, returns mutated population based on probability of percent argument (int)"""
    mutated_population = []
    for _, chromosome in enumerate(population):
        mutated_chromosome = []
        for _, gene in enumerate(chromosome):
            if random.randint(1, 100) <= percent:
                print("mutation!")
                if gene == 0:
                    gene = 1
                else:
                    gene = 0
            mutated_chromosome.append(gene)
        mutated_population.append(mutated_chromosome)
    return mutated_population


print(population)
population = mutation(population, 5)
print(population)

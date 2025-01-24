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


def read_data_from_row(row_number: int):
    weights = weights_list[row_number]
    values = values_list[row_number]
    capacity = capacities_list[row_number]
    return weights, values, capacity


weights, values, capacity = read_data_from_row(200)
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
    population_copy = population.copy()

    while len(population_copy) >= 2:

        chromosome_1 = random.choice(population_copy)
        population_copy.remove(chromosome_1)
        chromosome_2 = random.choice(population_copy)
        population_copy.remove(chromosome_2)

        if fitness(chromosome_1, weights, values, capacity) > fitness(chromosome_2, weights, values, capacity):
            tournament_winners.append(chromosome_1)
        else:
            tournament_winners.append(chromosome_2)

    if len(population_copy) == 1:
        tournament_winners.append(population_copy[0])

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
        while counter <= fitness(chromosome, weights, values, capacity):
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


def chromosome_weight(chromosome, weights):
    total_weight = 0

    for i, gene in enumerate(chromosome):
        if gene == 1:
            total_weight += weights[i]

    return total_weight


def chromosome_value(chromosome, values):
    total_value = 0

    for i, gene in enumerate(chromosome):
        if gene == 1:
            total_value += values[i]

    return total_value


def solution(weights: list[int], values: list[int], capacity: int):
    chromosome_solution = []
    all_possible_chromosomes = []
    all_possible_chromosomes.append([0, 0, 0, 0, 0])
    all_possible_chromosomes.append([0, 0, 0, 0, 1])
    all_possible_chromosomes.append([0, 0, 0, 1, 0])
    all_possible_chromosomes.append([0, 0, 0, 1, 1])
    all_possible_chromosomes.append([0, 0, 1, 0, 0])
    all_possible_chromosomes.append([0, 0, 1, 0, 1])
    all_possible_chromosomes.append([0, 0, 1, 1, 0])
    all_possible_chromosomes.append([0, 0, 1, 1, 1])
    all_possible_chromosomes.append([0, 1, 0, 0, 0])
    all_possible_chromosomes.append([0, 1, 0, 0, 1])
    all_possible_chromosomes.append([0, 1, 0, 1, 0])
    all_possible_chromosomes.append([0, 1, 0, 1, 1])
    all_possible_chromosomes.append([0, 1, 1, 0, 0])
    all_possible_chromosomes.append([0, 1, 1, 0, 1])
    all_possible_chromosomes.append([0, 1, 1, 1, 0])
    all_possible_chromosomes.append([0, 1, 1, 1, 1])
    all_possible_chromosomes.append([1, 0, 0, 0, 0])
    all_possible_chromosomes.append([1, 0, 0, 0, 1])
    all_possible_chromosomes.append([1, 0, 0, 1, 0])
    all_possible_chromosomes.append([1, 0, 0, 1, 1])
    all_possible_chromosomes.append([1, 0, 1, 0, 0])
    all_possible_chromosomes.append([1, 0, 1, 0, 1])
    all_possible_chromosomes.append([1, 0, 1, 1, 0])
    all_possible_chromosomes.append([1, 0, 1, 1, 1])
    all_possible_chromosomes.append([1, 1, 0, 0, 0])
    all_possible_chromosomes.append([1, 1, 0, 0, 1])
    all_possible_chromosomes.append([1, 1, 0, 1, 0])
    all_possible_chromosomes.append([1, 1, 0, 1, 1])
    all_possible_chromosomes.append([1, 1, 1, 0, 0])
    all_possible_chromosomes.append([1, 1, 1, 0, 1])
    all_possible_chromosomes.append([1, 1, 1, 1, 0])
    all_possible_chromosomes.append([1, 1, 1, 1, 1])
    chromosome_solution = all_possible_chromosomes[0]

    chromosome_solution_value = chromosome_value(chromosome_solution, values)
    for _, chromosome in enumerate(all_possible_chromosomes):
        if chromosome_value(chromosome, values) > chromosome_solution_value and chromosome_weight(chromosome, weights) <= capacity:
            chromosome_solution = chromosome
            chromosome_solution_value = chromosome_value(chromosome, values)
            print_chromosome(chromosome, weights, values)
    return chromosome_solution


def genetic_algorithm(population: list[list[int]], weights: list[int], values: list[int], capacity: int, selection: int, crossover: int, mutation_percent: int, generation_limit: int):
    """Genetic algorithm for knapsack problem, main function. Returns solution - chromosome (list[int])
    Arguments: population, weights, values, capacity,
        selection:
            1 - tournament selection,
            2 - roulette selection;
        crossover:
            1 - 1 point crossover,
            2 - 2 point crossover;
        mutation_percent - int(1-100),
        generation_limit - number of generations before stop.
    """
    print("\n\ngenetic algorithm")
    print("population size:", len(population))
    print("population: \n", population)
    print("weights:", weights)
    print("values:", values)
    print("capacity:", capacity)
    print("solution:", solution(weights, values, capacity))
    print("selection:", selection)
    print("crossover:", crossover)
    print("mutation percent:", mutation_percent)

    generation_counter = 0
    while generation_counter < generation_limit:
        new_population = []

        while len(new_population) < len(population):

            if selection == 1:
                winners = tournament_selection(
                    population, weights, values, capacity)
                father = random.choice(winners)
                mother = random.choice(winners)
                counter = 0
                while father == mother and counter < 3:
                    mother = random.choice(winners)
                    counter += 1
            elif selection == 2:
                father = roulette_selection(
                    population, weights, values, capacity)
                mother = roulette_selection(
                    population, weights, values, capacity)
                counter = 0
                while father == mother and counter < 3:
                    mother = roulette_selection(
                        population, weights, values, capacity)
                    counter += 1
            if crossover == 1:
                offspring_1, offspring_2 = crossover_1(father, mother, 3)
                new_population.append(offspring_1)
                new_population.append(offspring_2)
            elif crossover == 2:
                offspring_1, offspring_2 = crossover_2(father, mother, 2, 4)
                new_population.append(offspring_1)
                new_population.append(offspring_2)

        generation_counter += 1
        population = new_population
        population = mutation(population, mutation_percent)
        print(population)
    return 0


population = []
population = generate_starting_population(10)
weights, values, capacity = read_data_from_row(201)

print("solution:")
solution(weights, values, capacity)

genetic_algorithm(population, weights, values, capacity, 2, 2, 2, 10)

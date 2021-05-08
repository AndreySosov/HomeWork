import time
import random
import statistics

# Константы веса в граммах

GOAL = 50000
NUM_RATS = 20
INITIAL_MIN_WT = 200
INITIAL_MAX_WT = 600
INITIAL_MODE_WT = 300
MUTATE_ODDS = 0.01
MUTATE_MIN = 0.5
MUTATE_MAX = 1.2
LITTER_SIZE = 8
LITTER_PER_YEAR = 10
GENERATION_LIMIT = 500

# Обеспечить для племенных пар четное число крыс

if NUM_RATS % 2 != 0:
    NUM_RATS += 1

# Функция создающая первоначальную популяцию крыс

def populate(num_rats, min_wt, max_wt, mode_wt):
    '''Инициализировать популяцию треугольным распределением весов'''
    return [int(random.triangular(min_wt, max_wt, mode_wt)) for i in range(num_rats)]

def fitness(population, goal):
    '''Измерить пригодность популяции, основываясь на среднем значении атрибута
       относительно цели'''
    ave = statistics.mean(population)
    return ave / goal

def select(population, to_retain):
    '''Отбраковать популяцию, оставив только заданное число ее членов'''
    sorted_population = sorted(population)
    to_retain_by_sex = to_retain//2
    members_per_sex = len(sorted_population)//2
    females = sorted_population[:members_per_sex]
    males = sorted_population[members_per_sex:]
    selected_females = females[-to_retain_by_sex:]
    selected_males = males[-to_retain_by_sex:]
    return selected_males, selected_females

def breed(males, females, litter_size):
    '''Скрестить гены среди членов популяции'''
    random.shuffle(males)
    random.shuffle(females)
    children = []
    for males, females in zip(males, females):
        for child in range(litter_size):
            child = random.randint(females, males)
            children.append(child)
    return children

def mutate(children, mutate_odds, mutate_min, mutate_max):
    '''Случайно изменить веса крыс, используя входные шансы и дробные изменения'''
    for index, rat in enumerate(children):
        if mutate_odds >= random.random():
            children[index] = round(rat * random.uniform(mutate_min, mutate_max))
    return children

def main():
    '''Инициализировать популяцию, отобрать, вывести и мутировать, показать результаты'''
    generations = 0
    parents = populate(NUM_RATS, INITIAL_MIN_WT, INITIAL_MAX_WT, INITIAL_MODE_WT)
    print('Первоначальные веса популяции = {}'.format(parents))
    popl_fitness = fitness(parents, GOAL)
    print('Первоначальная приспособленность популяции = {}'.format(popl_fitness))
    print('Оставляемое число = {}'.format(NUM_RATS))

    ave_wt = []

    while popl_fitness < 1 and generations < GENERATION_LIMIT:
        selected_males, selected_females = select(parents, NUM_RATS)
        children = breed(selected_males, selected_females, LITTER_SIZE)
        children = mutate(children, MUTATE_ODDS, MUTATE_MIN, MUTATE_MAX)
        parents = selected_males + selected_females + children
        popl_fitness = fitness(parents, GOAL)
        print('Приспособленность поколения {} = {:.4f}'.format(generations, popl_fitness))
        ave_wt.append(int(statistics.mean(parents)))
        generations += 1

    print('Средний вес на поколение = {}'.format(ave_wt))
    print('\nЧисло поколений = {}'.format(generations))
    print('Число лет = {}'.format(int(generations / LITTER_PER_YEAR)))

if __name__ == '__main__':
    start_time = time.time()
    main()
    end_time = time.time()
    durarion = end_time - start_time
    print('\nВремя программы {} секунд.'.format(durarion))


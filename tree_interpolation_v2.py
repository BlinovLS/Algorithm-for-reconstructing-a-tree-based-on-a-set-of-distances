# Посроение графа с момощью библиотеки networkx

import networkx as nx
from networkx import Graph

import matplotlib
matplotlib.use('TkAgg')
import matplotlib.pyplot as plt
import scipy as sc

'''
Функция, которая рисует граф с помощью networkx

Делает:

1) Создаёт списко вершин с помощью Point.flag_number

2) Добавляет отношения медлу соответсвующими точками
'''


def draw_graph_with_newtworkx(mas_with_all_relations: list):
    mas_with_all_all_points_indexes = [index + 1 for index in range(Point.flag_number - 1)]

    tree = Graph()
    tree.add_nodes_from(mas_with_all_all_points_indexes)

    for relation in mas_with_all_relations:
        tree.add_edge(relation[0].flag_number, relation[1].flag_number)

    dictionary_of_start_pos = {
        1: (0.5, 1)
    }

    pos = nx.spring_layout(
        tree,
        pos=dictionary_of_start_pos,
        fixed=[1],
        method='energy',
        gravity=True
    )

    nx.draw(tree, pos, with_labels=True)
    plt.show()


# %%
# Геометричесский объект - точка
class Point():
    flag_number = 1  # Статическая переменная, которая даёт вершине личный (постоянный) номер

    def __init__(self, start_index=1):

        self.index: int

        self.index = start_index

        self.flag_number = Point.flag_number

        Point.flag_number += 1

    def change_index_to(self, new_index: int):
        '''
        Функция позволяет удобно менять рабочий (не постоянный) индекс данной точки

        :param new_index:
        :return: None
        '''

        self.index = new_index

    @staticmethod
    def print_flag_number(mas_with_all_relations: list):
        '''
        Функция выводит в консоль в человекочитаемом формате отношения между точками:
        из какой точки в какую проведено ребро

        :param mas_with_all_relations:
        :return: None
        '''

        if mas_with_all_relations:

            for relations in mas_with_all_relations:
                print(f'{relations[0].flag_number} --> {relations[1].flag_number}')
        else:
            print('nothing here')


# %%
# Обратный шаг --> возвращает связь вершин друг с другом

import numpy as np
import json

pass_to_file_with_history = 'history_of_identification.jsonl'

'''
Возвращает полную историю преобразований
История считывается из файла
'''


def from_file_read_full_history():
    mas_with_full_history = list()

    with open(pass_to_file_with_history, 'r') as file:
        for line in file:
            one_historic_step = json.loads(line)

            mas_with_full_history.append(one_historic_step)

    mas_with_full_history.reverse()

    return mas_with_full_history


'''
Обрабатывает одну пронумерованную точку:

Делает:

1) если связь, то создание новой точки и добавление её к вновь прибывшим 
!И! создание связи с ней

2) если не связь, то смена номера точки
'''


def processing_one_indexed_point(
        indexed_point: Point,
        j_r_for_one_point: list,
        c_j: list,
        list_with_new_points: list,
        list_with_all_relations: list
):
    for index in np.array(j_r_for_one_point) - 1:

        if c_j[index] != 0:

            new_point = Point()
            list_with_new_points.append(new_point)

            list_with_all_relations.append((indexed_point, new_point))

        else:

            indexed_point.change_index_to(index + 1)


'''
Обработка всех пронумерованных точек:

Делает:

1) идёт по всем нумерованным точкам

2) находит для каждой точки её j_r

3) обрабыьв=ывает эту точку (см. обработку выше)

4) удаление отработавших j_r (см. функцию ниже)
'''


def processing_ALL_indexed_points(
        mas_with_ALL_indexed_points_for_now: list,
        mas_with_ALL_j_r: list,
        mas_with_all_c_j: list,
        list_with_all_new_points: list,
        list_with_all_relations: list,
):
    j_r_for_delet = list()

    for indexed_point in mas_with_ALL_indexed_points_for_now:
        j_r_for_the_point = mas_with_ALL_j_r[indexed_point.index - 1]

        processing_one_indexed_point(
            indexed_point,
            j_r_for_the_point,
            mas_with_all_c_j,
            list_with_all_new_points,
            list_with_all_relations
        )

        j_r_for_delet.append(j_r_for_the_point)

    delet_all_extra_j_r(mas_with_ALL_j_r, j_r_for_delet)


'''
Удаление отработавших j_r

j_r отработал - значит он поучавствовал в построении связей для нумерованных точек
'''


def delet_all_extra_j_r(mas_with_all_j_r: list, j_r_for_delet: list):
    for j_r in j_r_for_delet:
        mas_with_all_j_r.remove(j_r)


'''
Обработка одной ненумерованной точки:

Делает:

1) идёт по индексам из j_r

2) если связь, то добавление новой точки 
!И! создание с ней связи

3) если нет связи, то приобретение номера 
!И! добавление к списку нумерованных точек
'''


def processing_one_UNindexed_point(
        UNindexed_point: Point,
        mas_with_ALL_indexed_points: list,
        j_r_for_one_point: list,
        c_j: list,
        list_with_new_points: list,
        list_with_all_relations: list
):
    for index in np.array(j_r_for_one_point) - 1:

        if c_j[index] != 0:

            new_point = Point()
            list_with_new_points.append(new_point)

            list_with_all_relations.append((UNindexed_point, new_point))

        else:

            UNindexed_point.change_index_to(index + 1)
            mas_with_ALL_indexed_points.append(UNindexed_point)


'''
Обработка всех Ненумерованных точек:

Делает:

1) Идёт по всем j_r

2) Из списка берёт одну ненумерованную точку

3) Обрабатывает её (см. выше)
'''


def processing_ALL_UNindexed_points(
        mas_with_ALL_UNindexed_points: list,
        mas_with_ALL_indexed_points: list,
        mas_with_ALL_j_r_that_is_remained: list,
        mas_with_all_c_j: list,
        list_with_all_new_points: list,
        list_with_all_relations: list
):
    index_of_UNindexd_point = 0

    for j_r in mas_with_ALL_j_r_that_is_remained:
        now_UNindexed_point = mas_with_ALL_UNindexed_points[index_of_UNindexd_point]

        processing_one_UNindexed_point(
            now_UNindexed_point,
            mas_with_ALL_indexed_points,
            j_r,
            mas_with_all_c_j,
            list_with_all_new_points,
            list_with_all_relations
        )

        index_of_UNindexd_point += 1


'''
Один шаг по истории:

1) обработка всех пронумерованных точек

2) обработка всех непронумерованных точек
'''


def one_step_of_reverse_procedure(
        one_history: list,
        mas_with_ALL_indexed_points: list,
        mas_with_ALL_Unindexed_points: list,
        mas_with_all_relations: list,
        mas_with_all_new_points: list
):
    global step

    Point.print_flag_number(mas_with_all_relations)
    print(f'{step} mas_with_ALL_indexed_points = {mas_with_ALL_indexed_points}')
    print(f'{step} mas_with_ALL_Unindexed_points = {mas_with_ALL_Unindexed_points}')

    mas_with_ALL_j_r, mas_with_all_c_j = one_history

    processing_ALL_indexed_points(
        mas_with_ALL_indexed_points,
        mas_with_ALL_j_r,
        mas_with_all_c_j,
        mas_with_all_new_points,
        mas_with_all_relations
    )

    print(f'{step} mas_with_all_new_points = {mas_with_all_new_points}')

    if mas_with_ALL_Unindexed_points:
        processing_ALL_UNindexed_points(
            mas_with_ALL_Unindexed_points,
            mas_with_ALL_indexed_points,
            mas_with_ALL_j_r,
            mas_with_all_c_j,
            mas_with_all_new_points,
            mas_with_all_relations
        )

    step += 1


'''
Функция --> результат работы этого модуля

Возвращает массив отношений вершин (из какой вершины, куда проведено ребро). 
'''


def full_reverse_procedure():
    full_history = from_file_read_full_history()

    mas_with_ALL_indexed_points = list()
    mas_with_ALL_Unindexed_points = list()

    mas_with_all_relations = list()

    mas_with_all_new_points = list()

    start_point = Point()

    mas_with_ALL_indexed_points.append(start_point)

    for one_history in full_history:
        # print(f'one_history = {one_history}')

        one_step_of_reverse_procedure(
            one_history,
            mas_with_ALL_indexed_points,
            mas_with_ALL_Unindexed_points,
            mas_with_all_relations,
            mas_with_all_new_points
        )

        # print(f'mas_with_all_new_points_0 = {mas_with_all_new_points}')

        mas_with_ALL_Unindexed_points = mas_with_all_new_points
        mas_with_all_new_points = []

        # print(f'mas_with_all_new_points = {mas_with_all_new_points}')
        # print(f'mas_with_ALL_Unindexed_points = {mas_with_ALL_Unindexed_points}')

    return mas_with_all_relations


step = 1
# %%
# Модуль для чтения матрицы расстояний

file_pass = 'matrix.txt'

'''
Читает матрицу из файла. 

Разделитель: ', '
'''


def read_from_file_matrix():
    matrix = list()

    with open('matrix.txt') as file:
        for line in file:
            matrix.append([int(integer_val) for integer_val in line.split(', ')])

    return matrix


# %%
# Модуль для записи истории преобразований

import numpy as np
import json

pass_to_file = 'history_of_identification.jsonl'
start_flag_isstart_was = False

'''
Создание новго файла
'''


def create_file():
    with open(pass_to_file, 'w+') as file:
        file.close()


'''
Функция - результат работы данного модуля:

записывает историю преобразований матрицы графа
'''


def write_one_step(mass_of_j_r, mass_of_c_j):
    global start_flag_isstart_was

    if not (start_flag_isstart_was):
        start_flag_isstart_was = True
        create_file()

    with open(pass_to_file, 'a') as file:
        file.write(json.dumps((mass_of_j_r, mass_of_c_j)) + '\n')


# %%
# Модуль для построения матрицы A_2 $corrected with Qwen$

import numpy as np

'''
Нахождение индексов отождествлённых строк (через группировку)
Возвращает:
- unique_representatives: список индексов (0-based), по которым строится A_2
- groups: список списков исходных индексов (1-based), объединённых в группы
'''


def get_identical_groups_and_representatives(B: list):
    B = np.array(B)
    n = B.shape[0]

    # Преобразуем каждую строку в хэшируемый вид (осторожно с float!)
    # Для надёжности можно использовать округление, если известно, что значения близки к целым
    # Здесь предполагаем, что B содержит точные значения (например, после корректного вычисления c_j)

    # Используем view для эффективного сравнения
    # Но проще: использовать np.unique с return_inverse
    _, unique_indices, inverse_indices = np.unique(B, axis=0, return_index=True, return_inverse=True)

    # Сортируем уникальные индексы, чтобы порядок был предсказуем
    unique_indices_sorted = sorted(unique_indices)

    # Построим группы: для каждого уникального индекса — список всех исходных индексов, ему соответствующих
    groups = [[] for _ in range(len(unique_indices_sorted))]
    # Создадим маппинг: какой уникальный индекс соответствует каждому значению inverse
    # Но проще: пройдём по всем исходным индексам
    for orig_idx in range(n):
        group_id = inverse_indices[orig_idx]
        # Найдём, какому уникальному индексу соответствует этот group_id
        # На самом деле, inverse_indices уже даёт номер группы
        # Но нам нужно сопоставить с сортированными представителями
        # Альтернатива: не сортировать, а использовать порядок из unique_indices

    # Проще: не сортировать, а использовать порядок, в котором np.unique возвращает уникальные строки
    unique_indices = unique_indices  # порядок, в котором встречаются уникальные строки
    groups = [[] for _ in range(len(unique_indices))]
    index_to_group = {}
    for group_id, idx in enumerate(unique_indices):
        index_to_group[idx] = group_id

    # Но inverse_indices уже даёт group_id напрямую!
    groups = [[] for _ in range(len(unique_indices))]
    for orig_idx in range(n):
        group_id = inverse_indices[orig_idx]
        groups[group_id].append(orig_idx + 1)  # 1-based для вывода

    return unique_indices, groups


'''
Операция отождествления матрицы B:
оставляем по одной строке и столбцу из каждой группы одинаковых
'''


def identification_B_matrix(B: list):
    B = np.array(B)
    unique_indices, _ = get_identical_groups_and_representatives(B)
    # Берём подматрицу по уникальным индексам (и строки, и столбцы!)
    A_2 = B[np.ix_(unique_indices, unique_indices)]
    return A_2.tolist()


'''
Функция - результат работы модуля:

Возвращает матрицу A_2 и список j_r - ых с отождествлёнными строками.
'''


def find_matrix_A_with_all_j_r(B: list):
    B = np.array(B)
    unique_indices, all_j_r = get_identical_groups_and_representatives(B)
    A_2 = B[np.ix_(unique_indices, unique_indices)].tolist()
    return A_2, all_j_r


# %%
# Модуль для построения вспомогательной матрицы B $corrected with Qwen$

import numpy as np

'''
Функция для нахождения c_j следующим образом:

min(P_j) / 2
'''


def find_one_c_j(P_j: list):
    return min(P_j) / 2


'''
Функция для нахождения всех c_j
'''


def find_all_c_j(mas_P_j: list):
    mas_c_j = list()

    for P_j in mas_P_j:
        mas_c_j.append(find_one_c_j(P_j))

    # print(f'mas_c_j = {mas_c_j}')
    return mas_c_j


'''
Нахождение элемента матрицы B следующим образом:

b_ij = a_ij - c_i - c_j
'''


def find_one_b_ij(A: list, mas_c_j: list, i: int, j: int):
    if i == j:
        return 0.0

    a_ij = A[i][j]
    c_i = mas_c_j[i]
    c_j = mas_c_j[j]

    b_ij = a_ij - c_i - c_j
    return b_ij


'''
Нахождение матрицы B
'''


def find_matrix_B(A: list, mas_c_j: list):
    n = len(A)
    B_matrix = []

    for i in range(n):
        one_line = []
        for j in range(n):
            b_ij = find_one_b_ij(A, mas_c_j, i, j)
            one_line.append(b_ij)
        B_matrix.append(one_line)

    return B_matrix


'''
Функция для вычисления P_j следующим образом:

a_ij + a_jk - a_ik, где i, k ∈ N \ {j}
(здесь N — множество индексов вершин, представленное как 0-based индексы)
'''


def find_one_P_j(A: list, j: int):
    n = len(A)
    # Исключаем j из множества индексов (работаем в 0-based системе)
    sub_indices = [idx for idx in range(n) if idx != j]

    P_j = []

    for i in sub_indices:
        for k in sub_indices:
            a_ij = A[i][j]
            a_jk = A[j][k]
            a_ik = A[i][k]
            P_j.append(a_ij + a_jk - a_ik)

    # print(f'P_j (for j={j}) = {P_j}')
    return P_j


'''
Функция для нахождения всех P_j
'''


def find_all_P_j(A: list):
    n = len(A)
    mas_with_all_P_j = []

    # Перебираем все вершины j в 0-based индексации
    for j in range(n):
        mas_with_all_P_j.append(find_one_P_j(A, j))

    # print(f'mas_with_all_P_j = {mas_with_all_P_j}')
    return mas_with_all_P_j


'''
Функция --> результат работы этого модуля:

Возвращает матрицу B и множество c_j-ых
'''


def B_matrix_with_all_c_j(A: list):
    # Определяем размер матрицы
    n = len(A)

    # Находим все P_j
    all_P_j = find_all_P_j(A)

    # Находим все c_j
    all_c_j = find_all_c_j(all_P_j)

    # Строим матрицу B
    B = find_matrix_B(A, all_c_j)

    return B, all_c_j


# %%
# Основная часть - Main программы


def direct_course():
    start_matrix_A = read_from_file_matrix()

    # print(np.array(start_matrix_A))

    size_of_matrix_A = start_matrix_A[0].__len__()

    now_matrix_A: list
    now_matrix_B: list
    now_mas_c_j: list
    now_mas_j_r: list

    now_matrix_A = start_matrix_A

    # print(now_matrix_A)

    while size_of_matrix_A > 2:
        now_matrix_B, now_mas_c_j = B_matrix_with_all_c_j(now_matrix_A)
        now_matrix_A, now_mas_j_r = find_matrix_A_with_all_j_r(now_matrix_B)

        # print(f'A = {now_matrix_A}')
        # print(f'now_mas_j_r = {now_mas_j_r}')

        write_one_step(now_mas_j_r, now_mas_c_j)

        size_of_matrix_A = now_matrix_A.__len__()

    print(f'A = {now_matrix_A}')


if __name__ == '__main__':
    direct_course()

    mas_with_all_relations = full_reverse_procedure()

    Point.print_flag_number(mas_with_all_relations)

    draw_graph_with_newtworkx(mas_with_all_relations)
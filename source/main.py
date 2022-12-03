from lessons import Lesson
from csp import *
from my_utils import *
import time

start_time = time.time()

#TODO: organizar e comentar código!!!

classes = {
    1: "LESI",
    2: "LESI-PL"
}

# numero de aulas total = turmas * 10

subjects =  {
    1: "Mobile",
    2: "Programming",
    3: "Test",
    4: "Teste2",
    5: "Teste3"
}

rooms = {
    0: "Online",
    1: "Sala L",
    2: "Sala T"
}

lessons_list = []
for x in range (len(classes)*10):
    new_l = Lesson(None, None, None, None, None, None)
    lessons_list.append(new_l)


dominio = {}


# cada turma tem de ter 10 aulas
# 0 - 9 e 10 - 19 e 20 - 29, etc. (10 lessons por class)
aux = 0
aux_final = 10


for x in classes:
    free_day = random.randint(2,6)
    dominio.update({f'L{aux}.fd': {free_day}}) # random day que será o dia livre da turma
    while aux != aux_final: # cada turma = 10 aulas
        dominio.update({f'L{aux}.c': {x}}) # assign às turmas (classes)
        aux+=1
    
    aux = aux_final
    aux_final = aux+10


for index, list_el in enumerate(lessons_list):
    dominio.update({f'L{index}.su': set(range(1,len(subjects)+1))}) # subjects
    dominio.update({f'L{index}.d': {2}}) # duration
    dominio.update({f'L{index}.w': set(range(2,7))}) # weekday
    dominio.update({f'L{index}.st': set(range(8,17))}) # start time
    dominio.update({f'L{index}.r': set(range(0,len(rooms)+1))}) # rooms

restricoes = [
    #Constraint(dominio.keys(), all_diff_constraint)
]


for x in range (0, (len(classes)*10)):
    for y in range (x+1, (len(classes)*10)):
        # L1.c = 1, L2.c = 1
        # L1.w = 2, L2.w = 2
        # [L1.st, L1.st+L1.d[ != L2.st   ou (L2.st >= L1.st+L1.d        ou L2.st + L2.d <= L1.st)
        # uma turma não pode ter duas aulas ao mesmo tempo no mesmo dia da semana 
        constraint_class_lesson_at_same_time = Constraint((f'L{x}.c', f'L{y}.c', f'L{x}.w', f'L{y}.w', f'L{x}.st', f'L{y}.st', f'L{x}.d', f'L{y}.d'), lambda lxc, lyc, lxw, lyw, lxst, lyst, lxd, lyd: (lxst >= (lyst + lyd) or lyst >= (lxst + lxd)) if(lxc == lyc and lxw == lyw) else True)


        # L1.su = 1, L2.su = 1
        # L1.w = 2, L2.w = 2
        # [L1.st, L1.st+L1.d[ != L2.st   ou (L2.st >= L1.st+L1.d        ou L2.st + L2.d <= L1.st)
        # uma disciplina (assumindo que uma disciplina é dada por um só professor) só pode estar em uma aula ao mesmo tempo
        constraint_subject_lesson_at_same_time = Constraint((f'L{x}.su', f'L{y}.su', f'L{x}.w', f'L{y}.w', f'L{x}.st', f'L{y}.st', f'L{x}.d', f'L{y}.d'), lambda lxsu, lysu, lxw, lyw, lxst, lyst, lxd, lyd: (lxst >= (lyst + lyd) or lyst >= (lxst + lxd)) if(lxsu == lysu and lxw == lyw) else True)
        

        # uma sala, a não ser que seja online, só pode estar numa aula ao mesmo tempo
        constraint_room_lesson_at_same_time = Constraint((f'L{x}.r', f'L{y}.r', f'L{x}.w', f'L{y}.w', f'L{x}.st', f'L{y}.st', f'L{x}.d', f'L{y}.d'), lambda lxr, lyr, lxw, lyw, lxst, lyst, lxd, lyd: (lxst >= (lyst + lyd) or lyst >= (lxst + lxd)) if(lxr == lyr and lxw == lyw and lxr != 0) else True)


        # no mesmo dia, só podem ser dadas aulas do mesmo tipo: online ou presencial
        # assim, garante que há, para além do dia livre, um dia de aulas online, reduzindo o número de viagens para o IPCA
        constraint_cant_book_presencial_on_same_day_of_online = Constraint((f'L{x}.c', f'L{y}.c', f'L{x}.w', f'L{y}.w', f'L{x}.r', f'L{y}.r'), lambda lxc, lyc, lxw, lyw, lxr, lyr : (lyr == 0 and lxr == 0) or (lyr != 0 and lxr != 0) if(lxc == lyc and lxw == lyw) else True)
    
        
        restricoes.append(constraint_class_lesson_at_same_time)
        restricoes.append(constraint_subject_lesson_at_same_time)
        restricoes.append(constraint_room_lesson_at_same_time)
        restricoes.append(constraint_cant_book_presencial_on_same_day_of_online) 
        

# print(get_only_list_of_attribute_from_class(1, "w"))

# print(dominio)


def constraint_one_to_two_online_lessons(*r_list):
    # print(r_list)
    if r_list.count(0) == 1 or r_list.count(0) == 2:
        # print("é verdade!", r_list)
        return True
    else:
        # print("é mentira!", r_list)
        return False 


def constraint_tree_lessons_per_day(*w_list):
    # print(w_list)
    for x in range(2,7):
        if (w_list.count(x) > 3):
            # print("FALSE", w_list)
            return False
    # print(w_list)
    return True


def constraint_random_free_day_per_week(*w_list):
    # print(w_list)
    random_day = w_list[-1]
    w_tuple_converted_to_list = list(w_list)
    w_tuple_converted_to_list.pop()

    # print(w_list)
    # print(random_day)
    if (w_tuple_converted_to_list.count(random_day) > 0):
        return False
    # print(w_list)
    # print(day)
    return True

def constraint_two_lessons_of_each_subject_per_week(*su_list):
    for x in subjects:
        if (su_list.count(x) != 2):
            # print("FALSE", su_list)
            return False
    # print(su_list)
    return True



for el in classes:
    # print(el)
    # uma turma tem de ter entre 1 a 2 aulas online por semana
    one_to_two_online_lessons_constraint = Constraint(tuple(get_only_list_of_attribute_from_class(el, "r")), constraint_one_to_two_online_lessons)
    restricoes.append(one_to_two_online_lessons_constraint)

    tree_lessons_per_day_constraint = Constraint(tuple(get_only_list_of_attribute_from_class(el, "w")), constraint_tree_lessons_per_day)
    restricoes.append(tree_lessons_per_day_constraint)

    random_free_day_per_week_constraint = Constraint(tuple(get_only_list_of_attribute_from_class(el, "w") + get_day_from_class(el, "fd")), constraint_random_free_day_per_week)
    restricoes.append(random_free_day_per_week_constraint)
    
    two_lessons_of_each_subject_per_week_constraint = Constraint(tuple(get_only_list_of_attribute_from_class(el, "su")), constraint_two_lessons_of_each_subject_per_week)
    restricoes.append(two_lessons_of_each_subject_per_week_constraint)





class_scheduling = NaryCSP(dominio, restricoes)
# print(class_scheduling.variables)
# print(ac_solver(class_scheduling, arc_heuristic=sat_up))
# dict_solver = ac_search_solver(class_scheduling, arc_heuristic=sat_up)
dict_solver = ac_solver(class_scheduling, arc_heuristic=sat_up)
print(dict_solver)
print("--- %s seconds ---" % (time.time() - start_time))
# TODO: passar dict final para algo mais "bonito"


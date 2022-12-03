from lessons import Lesson
from csp import *
from my_utils import *

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
    online_day = random.randint(2,6)
    while (online_day == free_day):
        online_day = random.randint(2,6)
    dominio.update({f'L{aux}.fd': {free_day}}) # random day que será o dia livre da turma
    dominio.update({f'L{aux}.od': {online_day}}) # random day que será o dia online da turma
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

        constraint_subject_lesson_at_same_time = Constraint((f'L{x}.su', f'L{y}.su', f'L{x}.w', f'L{y}.w', f'L{x}.st', f'L{y}.st', f'L{x}.d', f'L{y}.d'), lambda lxsu, lysu, lxw, lyw, lxst, lyst, lxd, lyd: (lxst >= (lyst + lyd) or lyst >= (lxst + lxd)) if(lxsu == lysu and lxw == lyw) else True)
        # L1.su = 1, L2.su = 1
        # L1.w = 2, L2.w = 2
        # [L1.st, L1.st+L1.d[ != L2.st   ou (L2.st >= L1.st+L1.d        ou L2.st + L2.d <= L1.st)
        # uma disciplina (assumindo que uma disciplina é dada por um só professor) só pode estar em uma aula ao mesmo tempo

        constraint_room_lesson_at_same_time = Constraint((f'L{x}.r', f'L{y}.r', f'L{x}.w', f'L{y}.w', f'L{x}.st', f'L{y}.st', f'L{x}.d', f'L{y}.d'), lambda lxr, lyr, lxw, lyw, lxst, lyst, lxd, lyd: (lxst >= (lyst + lyd) or lyst >= (lxst + lxd)) if(lxr == lyr and lxw == lyw and lxr != 0) else True)


        # a não ser que seja online, uma sala só pode estar numa aula ao mesmo tempo

        #constraint_cant_book_online_after_lesson = Constraint((f'L{x}.c', f'L{y}.c', f'L{x}.w', f'L{y}.w', f'L{x}.st', f'L{y}.st', f'L{x}.d', f'L{x}.r', f'L{y}.r'), lambda lxc, lyc, lxw, lyw, lxst, lyst, lxd, lxr, lyr : (lyr != 0) if(lxc == lyc and lxw == lyw and (lyst == (lxst + lxd)) and lxr != 0) else True)
        # uma aula online não pode ser logo depois de uma presencial 
        # backup... não usar (é uma função antiga, DEPRECATED! foi substituida pela de baixo)


        #constraint_cant_book_presencial_after_online_and_vice_versa = Constraint((f'L{x}.c', f'L{y}.c', f'L{x}.w', f'L{y}.w', f'L{x}.st', f'L{y}.st', f'L{x}.d', f'L{y}.d', f'L{x}.r', f'L{y}.r'), lambda lxc, lyc, lxw, lyw, lxst, lyst, lxd, lyd, lxr, lyr : (lyr == 0 and lxr == 0) or (lyr != 0 and lxr != 0) if(lxc == lyc and lxw == lyw and ((lyst == (lxst + lxd)) or (lxst == lyst + lyd))) else True)
        # uma aula, logo após a outra, deve ser do mesmo "tipo" de sala que a outra, ou seja:
        # se a primeira for online, a segunda é online
        # se a primeira for presencial, a segunda é presencial
        # TODO: em principio funciona, testar mais!!!
        # TODO: será trocado por um dia em que só haverá aulas online


        #constraint_cant_book_online_after_lesson_2 = Constraint((f'L{x}.c', f'L{y}.c', f'L{x}.w', f'L{y}.w', f'L{x}.st', f'L{y}.st', f'L{x}.d', f'L{x}.r', f'L{y}.r'), lambda lxc, lyc, lxw, lyw, lxst, lyst, lxd, lxr, lyr : (lxr == 0) if(lxc == lyc and lxw == lyw and (lyst == lxst + lxd) and lyr == 0) else True)
        # uma aula presencial não pode ser logo depois de uma online
        # backup... não usar (é uma função antiga, DEPRECATED! foi substituida pela de cima)

        # tres aulas num dia
        # constraint_tree_lessons_a_day = Constraint((f'L{x}.c', f'L{y}.c', f'L{x}.w', f'L{y}.w', f'L{x}.st', f'L{y}.st', f'L{x}.d'), lambda lxc, lyc, lxw, lyw, lxst, lyst, lxd: (lyst >= lxst - lxd*2 and lyst <= lxst) or (lyst <= lxst + lxd*2 and lyst >= lxst) if(lxc == lyc and lxw == lyw) else True)
        # DEPRECATED

        restricoes.append(constraint_class_lesson_at_same_time)
        restricoes.append(constraint_subject_lesson_at_same_time)
        restricoes.append(constraint_room_lesson_at_same_time)
        # restricoes.append(constraint_cant_book_online_after_lesson) 
        # restricoes.append(constraint_cant_book_online_after_lesson_2)
        # restricoes.append(constraint_cant_book_presencial_after_online_and_vice_versa) 
        # restricoes.append(constraint_tree_lessons_a_day)

   



# print(get_only_list_of_attribute_from_class(1, "w"))


# print(dominio)

def constraint_function_test(*c_list):
    print(c_list)
    return True
    #for e in c_list:
    #    if c_list.count(e) > 1:
    #        # print("ola")
    #        return True
    #    else:
    #        # print("adeus")
    #        return False


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


def constraint_random_day_for_online_lessons(*args):
    o_day = args[-1]
    args_tuple_to_list = list(args)
    args_tuple_to_list.pop() # remover o_day
    w_list = args_tuple_to_list[:10]
    r_list = args_tuple_to_list[10:]
    # print(o_day)
    # print(w_list)
    # print(r_list)
    # print(args)
    for index, el in enumerate(r_list):
        if el == 0: # aula online
            if w_list[index] != o_day: # se for num dia que não o dia de aulas online
                # print("FALSE!")
                # print(o_day)
                # print(w_list)
                # print(r_list)
                # print(args)
                return False
        else: # aula presencial
            if w_list[index] == o_day: # se for num dia que é dia de aulas online
                return False
    # print("TRUE!")
    # print(o_day)
    # print(w_list)
    # print(r_list)
    # print(args)
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
    random_online_day_per_week_constraint = Constraint(tuple(get_only_list_of_attribute_from_class(el, "w") + get_only_list_of_attribute_from_class(el, "r") + get_day_from_class(el, "od")), constraint_random_day_for_online_lessons)
    restricoes.append(random_online_day_per_week_constraint)








class_scheduling = NaryCSP(dominio, restricoes)
# print(class_scheduling.variables)
# print(ac_solver(class_scheduling, arc_heuristic=sat_up))
# dict_solver = ac_search_solver(class_scheduling, arc_heuristic=sat_up)
dict_solver = ac_solver(class_scheduling, arc_heuristic=sat_up)
print(dict_solver)
# TODO: passar dict final para algo mais "bonito"


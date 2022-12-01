from lessons import Lesson
from csp import *

classes = {
    1: "LESI",
    2: "LESI-PL"
}

# numero de aulas total = turmas * 10

subjects =  {
    1: "Mobile",
    2: "Programming",
    3: "Test"
}

rooms = {
    0: "Online",
    1: "Sala L",
    2: "Sala T"
}

list = []
for x in range (len(classes)*10):
    new_l = Lesson(None, None, None, None, None, None)
    list.append(new_l)


dominio = {}


# cada turma tem de ter 10 aulas
# 0 - 9 e 10 - 19 e 20 - 29, etc. (10 lessons por class)
aux = 0
aux_final = 10
for x in classes:
    while aux != aux_final:
        dominio.update({f'L{aux}.c': {x}}) # classes
        aux+=1
    aux = aux_final
    aux_final = aux+10


for index, list_el in enumerate(list):
    dominio.update({f'L{index}.su': set(range(1,len(subjects)+1))}) # subjects
    dominio.update({f'L{index}.d': {2}}) # duration
    dominio.update({f'L{index}.w': set(range(2,7))}) # weekday
    dominio.update({f'L{index}.st': set(range(8,17))}) # start time (apenas horas certas? <- TODO: ver isto)
    dominio.update({f'L{index}.r': set(range(1,len(rooms)+1))}) # rooms


restricoes = [
    #Constraint(dominio.keys(), all_diff_constraint)
]

for x in range (0, 20):
    for y in range (x+1, 20):
        # L1.c = 1, L2.c = 1
        # L1.w = 2, L2.w = 2
        # [L1.st, L1.st+L1.d[ != L2.st   ou (L2.st >= L1.st+L1.d        ou L2.st + L2.d <= L1.st)
        # uma turma não pode ter duas aulas ao mesmo tempo no mesmo dia da semana 
        constraint_lesson_same_time = Constraint((f'L{x}.c', f'L{y}.c', f'L{x}.w', f'L{y}.w', f'L{x}.st', f'L{y}.st', f'L{x}.d', f'L{y}.d'), lambda lxc, lyc, lxw, lyw, lxst, lyst, lxd, lyd: (lxst >= (lyst + lyd) or lyst >= (lxst + lxd)) if(lxc == lyc and lxw == lyw) else True)
        restricoes.append(constraint_lesson_same_time)



# print(dominio)




class_scheduling = NaryCSP(dominio, restricoes)
# print(class_scheduling.variables)
print(ac_solver(class_scheduling, arc_heuristic=sat_up))


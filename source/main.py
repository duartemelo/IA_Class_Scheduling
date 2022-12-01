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


for index, list_el in enumerate(list):
    dominio.update({f'L{index}.c': set(range(1,len(classes)+1))}) # classes 
    dominio.update({f'L{index}.su': set(range(1,len(subjects)+1))}) # subjects
    dominio.update({f'L{index}.d': {120}}) # duration
    dominio.update({f'L{index}.w': set(range(2,7))}) # weekday
    dominio.update({f'L{index}.st': set(range(8,17))}) # start time (apenas horas certas? <- TODO: ver isto)
    dominio.update({f'L{index}.r': set(range(1,len(rooms)+1))}) # rooms



# L1.c = 1, L2.c = 1
# L1.w = 2, L2.w = 2
# [L1.st, L1.st+L1.d[ != L2.st   ou (L2.st >= L1.st+L1.d        ou L2.st + L2.d <= L1.st)




print(dominio)



restricoes = [
    #Constraint(dominio.keys(), all_diff_constraint)
]

class_scheduling = NaryCSP(dominio, restricoes)
#print(class_scheduling.variables)
#print(ac_solver(class_scheduling, arc_heuristic=sat_up))




#l1 = Lesson(1, 1, 1, 1, 1, 1)
#print(l1)
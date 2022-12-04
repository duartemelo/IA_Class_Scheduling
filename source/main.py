from lessons import Lesson
from csp import *
from my_utils import *
import time

# start_time of execution
start_time = time.time()

# classes used in the algorithm, the name is irrelevant since only the numbers will be used
classes = {
    1: "LESI",
    2: "LESI-PL"
}

# subjects used in the algorithm, the algorithm accepts, at the moment, 5 subjects, the name is irrelevant
subjects =  {
    1: "Mobile",
    2: "Programming",
    3: "Test",
    4: "Teste2",
    5: "Teste3"
}

# rooms used in the algorithm, the name is irrelevant but ROOM 0 = online!
rooms = {
    0: "Online",
    1: "Sala L",
    2: "Sala T",
    3: "Sala N"
}

rooms_usages = {}
for room in rooms.keys():
    if room != 0:
        rooms_usages[room] = 0


# each class has 10 lessons per week
lessons_list = []
for x in range (len(classes)*10):
    # Lesson is class that was created when we started coding this project
    # It is kinda irrelevant / unused at the moment, so it could be removed (TODO: remove?)
    new_l = Lesson(None, None, None, None, None, None)
    lessons_list.append(new_l)


# Domain defines the domain of each variable
domain = {}

# each class has 10 lessons
# Lesson 0-9 corresponds to Class 1
# Lesson 10-19 corresponds to Class 2...
# etc.
aux = 0
aux_final = 10
for x in classes:
    free_day = random.randint(2,6)
    # print(rooms_usages)
    room = least_used_room(rooms_usages)
    rooms_usages[room]+=1
    # print(rooms_usages)
    domain.update({f'L{aux}.fd': {free_day}}) # each class has a random day without lessons
    domain.update({f'L{aux}.fr': {room}}) # each class has a random day without lessons
    while aux != aux_final: 
        domain.update({f'L{aux}.c': {x}}) # assigning lessons to classes
        aux+=1
    
    aux = aux_final
    aux_final = aux+10


for index, list_el in enumerate(lessons_list):
    domain.update({f'L{index}.su': set(range(1,len(subjects)+1))}) # subjects domain assign
    domain.update({f'L{index}.d': {2}}) # duration domain assign 
    domain.update({f'L{index}.w': set(range(2,7))}) # weekday domain assign
    domain.update({f'L{index}.st': set(range(8,17))}) # start time domain assign
    domain.update({f'L{index}.r': set(range(0,len(rooms)+1))}) # rooms domain assign

# Problem' constraints / restrictions
restrictions = [
    #Constraint(domain.keys(), all_diff_constraint)
]


# Assigning constraints to lessons
# L1 -> L2, L1 -> L3, L1 -> L4 , etc..
# L2 -> L3, L2 -> L4, etc..
# etc.. 
for x in range (0, (len(classes)*10)):
    for y in range (x+1, (len(classes)*10)):
        # L1.c = 1, L2.c = 1
        # L1.w = 2, L2.w = 2
        # [L1.st, L1.st+L1.d[ != L2.st   ou (L2.st >= L1.st+L1.d        ou L2.st + L2.d <= L1.st)
        # a class can't be in two lessons at the same time
        constraint_class_lesson_at_same_time = Constraint((f'L{x}.c', f'L{y}.c', f'L{x}.w', f'L{y}.w', f'L{x}.st', f'L{y}.st', f'L{x}.d', f'L{y}.d'), lambda lxc, lyc, lxw, lyw, lxst, lyst, lxd, lyd: (lxst >= (lyst + lyd) or lyst >= (lxst + lxd)) if(lxc == lyc and lxw == lyw) else True)


        # L1.su = 1, L2.su = 1
        # L1.w = 2, L2.w = 2
        # [L1.st, L1.st+L1.d[ != L2.st   ou (L2.st >= L1.st+L1.d        ou L2.st + L2.d <= L1.st)
        # a subject (assuming that a teacher is assigned to a subject) can't be in two lessons at the same time
        constraint_subject_lesson_at_same_time = Constraint((f'L{x}.su', f'L{y}.su', f'L{x}.w', f'L{y}.w', f'L{x}.st', f'L{y}.st', f'L{x}.d', f'L{y}.d'), lambda lxsu, lysu, lxw, lyw, lxst, lyst, lxd, lyd: (lxst >= (lyst + lyd) or lyst >= (lxst + lxd)) if(lxsu == lysu and lxw == lyw) else True)
        

        # a room (except online), can't be in two lessons at the same time
        constraint_room_lesson_at_same_time = Constraint((f'L{x}.r', f'L{y}.r', f'L{x}.w', f'L{y}.w', f'L{x}.st', f'L{y}.st', f'L{x}.d', f'L{y}.d'), lambda lxr, lyr, lxw, lyw, lxst, lyst, lxd, lyd: (lxst >= (lyst + lyd) or lyst >= (lxst + lxd)) if(lxr == lyr and lxw == lyw and lxr != 0) else True)


        # in the same day, a class can have either online or presencial lessons
        # by doing this, we reduce the number of trips to IPCA
        constraint_cant_book_presencial_on_same_day_of_online = Constraint((f'L{x}.c', f'L{y}.c', f'L{x}.w', f'L{y}.w', f'L{x}.r', f'L{y}.r'), lambda lxc, lyc, lxw, lyw, lxr, lyr : (lyr == 0 and lxr == 0) or (lyr != 0 and lxr != 0) if(lxc == lyc and lxw == lyw) else True)
    
        
        # adding previous created restrictions
        restrictions.append(constraint_class_lesson_at_same_time)
        restrictions.append(constraint_subject_lesson_at_same_time)
        restrictions.append(constraint_room_lesson_at_same_time)
        restrictions.append(constraint_cant_book_presencial_on_same_day_of_online) 
        

# print(get_only_list_of_attribute_from_class(1, "w"))

# print(domain)


# each class has one to two online lessons per week
def constraint_one_to_two_online_lessons(*r_list):
    if r_list.count(0) == 1 or r_list.count(0) == 2:
        return True
    else:
        return False 


# each class has a maximum of 3 lessons per day
def constraint_tree_lessons_per_day(*w_list):
    for x in range(2,7):
        if (w_list.count(x) > 3):
            return False
    return True


# each class has a random free day (day without lessons) per week, this reduces trips to IPCA
def constraint_random_free_day_per_week(*w_list):
    random_day = w_list[-1]
    w_tuple_converted_to_list = list(w_list)
    w_tuple_converted_to_list.pop()

    
    if (w_tuple_converted_to_list.count(random_day) > 0):
        return False
    return True


# each class has two lessons of each subject per week (5 subjects * 2 lessons = 10 lessons)
def constraint_two_lessons_of_each_subject_per_week(*su_list):
    for x in subjects:
        if (su_list.count(x) != 2):
            return False
    return True


# each class has two to four lessons in a specific classroom
def constraint_two_to_four_lessons_in_specific_classroom(*r_list):
    favourite_room = r_list[-1]
    r_tuple_converted_to_list = list(r_list)
    r_tuple_converted_to_list.pop()

    if r_list.count(favourite_room) >= 2 and r_list.count(favourite_room) <= 4:
        return True
    return False


# adding previous function constraints to restrictions array
for el in classes:
    one_to_two_online_lessons_constraint = Constraint(tuple(get_only_list_of_attribute_from_class(el, "r")), constraint_one_to_two_online_lessons)
    restrictions.append(one_to_two_online_lessons_constraint)

    tree_lessons_per_day_constraint = Constraint(tuple(get_only_list_of_attribute_from_class(el, "w")), constraint_tree_lessons_per_day)
    restrictions.append(tree_lessons_per_day_constraint)

    random_free_day_per_week_constraint = Constraint(tuple(get_only_list_of_attribute_from_class(el, "w") + get_day_from_class(el, "fd")), constraint_random_free_day_per_week)
    restrictions.append(random_free_day_per_week_constraint)
    
    two_lessons_of_each_subject_per_week_constraint = Constraint(tuple(get_only_list_of_attribute_from_class(el, "su")), constraint_two_lessons_of_each_subject_per_week)
    restrictions.append(two_lessons_of_each_subject_per_week_constraint)

    two_to_four_lessons_in_specific_classroom_constraint = Constraint(tuple(get_only_list_of_attribute_from_class(el, "r") + get_day_from_class(el, "fr")), constraint_two_to_four_lessons_in_specific_classroom)
    restrictions.append(two_to_four_lessons_in_specific_classroom_constraint)




class_scheduling = NaryCSP(domain, restrictions)
# print(class_scheduling.variables)
# print(ac_solver(class_scheduling, arc_heuristic=sat_up))
# dict_solver = ac_search_solver(class_scheduling, arc_heuristic=sat_up)
dict_solver = ac_solver(class_scheduling, arc_heuristic=sat_up)
print(dict_solver)
print("--- %s seconds ---" % (time.time() - start_time))
def get_only_list_of_attribute_from_class(c, attribute):
    final_list = []
    x = (c-1)*10
    x_max = c*10-1
    # print(x)
    # print(x_max)
    while (x <= x_max):
        final_list.append(f'L{x}.{attribute}')
        x+=1
    return final_list


def get_random_day_from_class(c):
    x = (c-1)*10
    random_day=f'L{x}.rd'
    return [random_day]
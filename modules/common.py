import random


def get_random_list(list_org):
    list_new = []
    while len(list_org) > 0:
        index = random.randint(0, len(list_org) - 1)
        list_new.append(list_org[index])
        list_org.pop(index)
    return list_new

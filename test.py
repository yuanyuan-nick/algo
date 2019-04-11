def add_end(L=None):
    if L is None:
        L = []
    L.append('END')
    return L

print(add_end([1,2]))

print(add_end())

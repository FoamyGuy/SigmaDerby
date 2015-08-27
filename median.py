def med(x):
    m,r= divmod(len(x),2)
    if r:
        return sorted(x)[m]
    return sorted(x)[m+1]
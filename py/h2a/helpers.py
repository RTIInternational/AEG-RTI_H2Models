#
# This file is programmatically generated by py_writer.py; do not edit
#
def get(obj, key):
    return obj[key]

def concat(a, b):
    return a + b

def split(a, b):
    return a.split(b)

def npv(r, cfList):
    sum_pv = 0
    for i, pmt in enumerate(cfList, start=1):
        sum_pv += pmt / ((1 + r) ** i)
    return sum_pv

def skip(a, b):
    return a[b:]

def seq_along(a):
    return range(len(a))

TRUE = True
YEAR_1 = 0
YEAR_2 = 1
YEAR_3 = 2
YEAR_4 = 3

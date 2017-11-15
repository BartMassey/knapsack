#!/usr/bin/python3
# Copyright (c) 2017 Bart Massey
# [This program is licensed under the "MIT License"]
# Please see the file LICENSE in the source
# distribution of this software for license terms.

# Knapsack solver using DFS

from sys import argv
from random import randrange

# A Knapsack Problem instance.
class Knapsack(object):

    # `c` and `n` are given capacity and number of
    # items. The value and weight of each item is chosen
    # randomly from the range 1..maxv.
    def __init__(self, c, n, maxv=100):
        self.c = c
        self.n = n
        def randattr():
            return [randrange(1, maxv + 1) for _ in range(n)]
        self.v = randattr()
        self.w = randattr()

    # Combine the attribute list to get a single list of
    # item attributes.
    def items(self):
        return [(i, self.w[i], self.v[i]) for i in range(self.n)]

# Return a list of all sets of elements drawn
# from the given input collection `l`.
def powerset(l):
    result = [set()]
    while l:
        e = l.pop(0)
        result += [s | {e} for s in result]
    return result

# Compute the maximum legal knapsack value for instance `ks`
# using truly ignorant brute-force.
def ks_brute_force(ks):
    # Maximum packing and value found so far.
    max_t = set()
    max_val = 0

    # Compute the sum of all attributes `a` at indices
    # drawn from the collection `t`.
    def fsum(a, t):
        result = 0
        for e in t:
            result += a[e]
        return result

    # Try every possible subset of 1..n.
    for t in powerset(list(range(ks.n))):
        # Check capacity.
        if fsum(ks.w, t) > ks.c:
            continue
        # Find value.
        val = fsum(ks.v, t)
        # Update max value if needed.
        if val > max_val:
            max_val = val
            max_t = t
    # Return max value.
    return (max_t, max_val)

# Compute the maximum legal knapsack value for instance `ks`
# using complete search in state space of partial solutions
# with appropriate heurstics and pruning. If `bb` is `True`,
# do "branch-and-bound" pruning to speed up search.
def ks_dfs(ks, bb=False):
    # Maximum packing and value found so far.
    max_t = set()
    max_val = 0

    # Consider items in order of decreasing value density.
    def density(x):
        i, w, v = x
        return float(v) / float(w)
    S = [i for i, _, _ in sorted(ks.items(), key=density, reverse=True)]
    n = len(S)
    
    # Insert the next best item into the knapsack, or not.
    # Update the best solution if needed. `i` is current
    # item, `T` is set of items added so far, `val` and
    # `weight` are the running value and weight of `T`.
    def ks_dfs_step(i, T, val, weight):
        # Update best solution if needed.
        nonlocal max_t, max_val
        if val > max_val:
            max_val = val
            max_t = T
        # If there are no more items, we're done.
        if i >= n:
            return
        # Find the actual index of the i'th item.
        j = S[i]
        # Implement Branch-and-Bound.
        if bb:
            # Terrible heuristic: assume can fill rest
            # of basket with most dense remaining item.
            j_density = ks.v[j] / ks.w[j]
            optimum_rest = (ks.c - weight) * j_density
            if val + optimum_rest <= max_val:
                return
        # Calculate the potential weight with new item.
        new_weight = weight + ks.w[j]
        # If there's room, try adding the new item.
        if new_weight <= ks.c:
            ks_dfs_step(i + 1, T | {j}, val + ks.v[j], new_weight)
        # Try not adding the new item.
        ks_dfs_step(i + 1, T, val, weight)

    # Search all the feasibly optimal solutions and return
    # the best.
    ks_dfs_step(0, set(), 0, 0)
    return (max_t, max_val)

# Do a thing with the code above.
if argv[1] == "test":
    for _ in range(1000):
        ks = Knapsack(100, 10)
        sbf, wbf = ks_brute_force(ks)
        sdfs, wdfs = ks_dfs(ks)
        sdfsbb, wdfsbb = ks_dfs(ks, bb=True)
        if wbf != wdfs or wbf != wdfsbb:
            print(ks.items())
            print("", wbf)
            print("", wdfs)
            print("", wdfsbb)
elif argv[1] == "time":
    if argv[2] == "bf":
        ks = Knapsack(1000, 20)
        print(ks.items(), ks_brute_force(ks))
    elif argv[2] == "dfs":
        ks = Knapsack(1000, 20)
        print(ks.items(), ks_dfs(ks))
    elif argv[2] == "dfsbb":
        ks = Knapsack(1000, 20)
        print(ks.items(), ks_dfs(ks, bb=True))
    else:
        exit("unknown timer", argv[2])
else:
    exit("unknown action", argv[1])

def knapsack(capacity, items):
    svr = sorted([(value/size,size,value) for size,value in items],reverse=True)
    knapsack = [0]*len(items)
    for svr,size,value in svr:
        while True:
            if capacity - size >= 0:
                knapsack[items.index((size,value))] += 1
                capacity -= size
            else:
                break
    return knapsack

print(knapsack(100,[(1,1),(3,3)]))
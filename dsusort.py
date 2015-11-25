dsu = lambda iter,key=lambda x: x: [item for kv,item in sorted([(key(item),item) for item in iter])]


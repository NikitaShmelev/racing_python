from itertools import compress, product


def combinations(items):
    return list( set(compress(items,mask)) for mask in product(*[[0,1,3]]*len(items)) )

items = 'LRUD'
res =combinations(items)
i = 0
for item in res:
    if len(item) == 4:
        i+=1
        print(item)



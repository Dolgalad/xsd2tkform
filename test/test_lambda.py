

def foo(x):
    print(x)

funcs=[]
for i in range(10):
    funcs.append(lambda i=i: foo(i))

for f in funcs:
    f()

# Substring from String between two known chars
def substr_between(left, right):
    return string[string.find(left)+1:string.find(right)]

# quick functions to use for finding millisecond time difference
def time_start():
    global time
    import time
    global time_var 
    time_var = time.time()*1000
def time_end():
    print(round(time.time()*1000-time_var),'ms')

# run a file in REPL (Python terminal) to interact/test
# > python -i filename.py

def app(l):
    l.append(0)

li=[1]
app(li)
print(li)
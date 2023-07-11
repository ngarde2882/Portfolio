def swap(nums, i, j): # swaps position of 2 values in an array
        x = nums[i]
        nums[i] = nums[j]
        nums[j] = x


def timeConversion(s):
    # Write your code here
    o = ''
    if s[-2:]=='AM':
        if s[0:2]!='12':
            o += s[0:3]
        else:
            o += '00:'
    else:
        o += str(int(s[0:2])+12) + ':'
    o += s[3:8]
    return o

# print(timeConversion('12:45:54PM'))

def list_to_dict(l):
    d = {}
    # for i in range(start, stop, step)
    for i in range(0,len(l),1):
        if l[i] not in d:
            d[l[i]] = 1
        else:
            d[l[i]] += 1
    return d

def list_to_dict_with_location(l):
    d = {}
    # for i in range(start, stop, step)
    for i in range(0,len(l),1):
        if l[i] not in d:
            d[l[i]] = {'num':1,'loc':[i+1]}
        else:
            d[l[i]]['num'] += 1
            d[l[i]]['loc'].append(i+1)
    return d

def factors(m):
    l = []
    for i in range(1,m+1,1):
        if m%i==0:
            l.append(i)
    return l

def factor_pairs(m):
    l = factors(m)
    out = []
    for i in range(int(len(l)/2)):
        out.append((l[i],l[len(l)-1-i]))
    if len(l)%2==1:
        out.append((l[int(len(l)/2)],l[int(len(l)/2)]))
    return out

print(list_to_dict_with_location([1,1,1,2,3,4,7]))
print(factor_pairs(12))
print(factor_pairs(9))
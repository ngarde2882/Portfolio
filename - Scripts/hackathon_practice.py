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

# print(list_to_dict_with_location([1,1,1,2,3,4,7]))
# print(factor_pairs(12))
# print(factor_pairs(9))

# s = 'abcba'
s = 'abccba'
def expand(l,r):
    while l>=0 and r<len(s) and s[l]==s[r]:
        l-=1
        r+=1
    return s[l+1:r]
# print(expand(5,6))

def combinationSum(candidates, target):
    out = set()
    
    def backtrack(t, comb):
        nonlocal out, candidates
        for i in range(len(candidates)+1):
            if candidates[-i]>t:
                pass
            elif candidates[-i]==t:
                out.add(tuple(sorted(comb+[t])))
            elif candidates[-i]<t:
                backtrack(t-candidates[-i], comb+[candidates[-i]])
        
    backtrack(target, [])
    return out
# print(combinationSum([2,3,6,7], 9))

height = [1,0,2,1,0,1,3,2,1,2,1]
def recur(h,l,r):
    i = (height.index(max(h)))
    print(h[0:i],h[i],h[i+1:])
# recur(height,0,len(height)-1)
m = height.index(max(height))
h = height[m+1:]

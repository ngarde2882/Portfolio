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
        if s[0:2]=='12':
            o += s[0:3]
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
def miniMaxSum(arr):
    mini = min(arr)
    maxi = max(arr)
    summy = 0
    for i in arr:
        sum+=i
    print(summy-maxi,summy-mini)

# miniMaxSum([1,2,3,4,5])

def lonelyinteger(a):
    d = {}
    for i in a: # O(N)
        if i in d: # O(1)
            d[i]+=1
        else:
            d[i]=1
    # d = {i:# of i,}
    print(d)
    return min(d.values())

# print(lonelyinteger([1,2,3,2,1]))

def countingSort(arr):
    result = [0]*(max(arr)+1)
    print(result)
    for i in arr:
        result[i] += 1
    print(result)

def print_diamond(size):
    if size==1:
        print('a')
        return
    l = ['-','a','b','c','d','e','f','g','h','i','j','k','l','m','n','o','p','q','r','s','t','u','v','w','x','y','z']
    space = 2*size - 2
    q = []
    for i in range(size):
        string = l[0]*(space-2*i)
        temp = ''
        for j in range(i+1):
            string += l[size-j]
            string += l[0]
        string+=string[-4::-1]
        q.append(string)
    for i in q:
        print(i)
    for i in q[-2::-1]:
        print(i)

def cap_front(s):
    o = ''
    b=True
    for i in s:
        if b:
            b=False
            if (ord(i)>96) and (ord(i)<123):
                o += chr(ord(i)-32)
            else:
                o += i
        else:
            o += (i)
        if i==' ':
            b=True
    return o

def substring_game(s):
    v=0
    c=0
    d={}
    vowels = ['A','E','I','O','U']
    for i in range(len(s)):
        j=i+1
        while j <= len(s):
            if s[i:j] in d:
                d[s[i:j]] += 1
            else:
                d[s[i:j]] = 1
            j+=1
    for key,val in d.items():
        if key[0] in vowels:
            v+=val
        else:
            c+=val
    if c>v:
        print(f'Stuart {c}')
    elif v>c:
        print(f'Kevin {v}')
    else:
        print('Draw')
    print(d)

def myAtoi(s):
        out = 0
        neg, pos = False, False
        for i in range(len(s)):
            if s[i] == ' ':
                continue
            if neg and pos:
                return 0
            if s[i]>='0' and s[i]<='9':
                n = int(s[i])
                if out == 0:
                    out = -1*n if neg else n
                    continue
                out = int(str(out)+s[i])
                print(out)
                if out>=2147483647:
                    return 2147483647
                if out<=-2147483648:
                    return -2147483648
            else:
                if out>0:
                    return out
                if s[i]=='+':
                    pos = True
                    continue
                if s[i]=='-':
                    neg = True
                    continue
        return out

def center_target_for(s):
    length = len(s)
    if length==0:
        return ''
    c=int(length/2)
    l = c-1
    r = c if length//2==0.0 else c+1

    print(length,l,c,r)
    return 1

def Sum3(nums):
    print(nums)
    out = []
    P = set()
    N = set()
    p = []
    n = []
    z = 0
    for i in range(len(nums)):
        if nums[i]>0:
            P.add(nums[i])
            p.append(nums[i])
        elif nums[i]<0:
            N.add(nums[i])
            n.append(nums[i])
        else:
            z += 1
    
    if z>0:
        for val in p:
            if -1*val in N:
                out.append([-1*val,0,val])
    if z>2:
        out.append([0,0,0])
    
    for i in range(len(n)):
        for j in range(i+1,len(n)):
            target = -1*(n[i]+n[j])
            if target in P:
                out.append([n[i],n[j],target])

    for i in range(len(p)):
        for j in range(i+1,len(p)):
            target = -1*(p[i]+p[j])
            if target in N:
                out.append([p[i],p[j],target])
    
    return out

# print(center_target_for('1234567890'))
# print(4,int(4/2),[0,1,2,3])
# print(5,int(5/2),[0,1,2,3,4])

# print('\n'+str(myAtoi('apple123')))
# print(Sum3([-1,0,1,2,-1,-4]))


def isValid(s):
        q = []
        for i in s:
            if i in {'(','[','{'}:
                q.append(i)
            elif i==')':
                if q:
                    if q[len(q)-1]=='(':
                        q.pop()
                    else: return False
                else:
                    return False
            elif i==']':
                if q:
                    if q[len(q)-1]=='[':
                        q.pop()
                    else: return False
                else:
                    return False
            elif i=='}':
                if q:
                    if q[len(q)-1]=='{':
                        q.pop()
                    else: return False
                else:
                    return False
        if len(q)==0:
            return True
        return False

# print(isValid(']'))

# dic = {0:'a',1:'b',2:None,3:'d'}
# for k,v in dic.items():
#     if not v:
#         del dic[k]
# print(dic)

class ListNode:
    def __init__(self, val=0, next=None):
        self.val = val
        self.next = next

def mergeKLists(lists):
    dic = {}
    mini_val = 10**4+1
    mini_index = 51
    for i in range(len(lists)):
        print(lists[i].val)
        if lists[i]:
            dic[i] = lists[i]
            print(dic)
            if mini_val>lists[i].val:
                mini_val = lists[i].val
                mini_index = i
    out = ListNode(dic[mini_index].val)
    dic[mini_index] = dic[mini_index].next
    bus = out
    print(dic)
    while dic:
        l = []
        mini_val = 10**4+1
        mini_index = 51
        mt = []
        for k,v in dic.items():
            if not v:
                mt.append(k)
                continue
            if v.val<mini_val:
                mini_val = v.val
                mini_index = k
        bus.next = ListNode(mini_val)
        bus = bus.next
        print(dic)
        dic[mini_index] = dic[mini_index].next
        if not dic[mini_index]:
            mt.append(mini_index)
        for i in mt:
            del dic[i]
        if not dic:
            break
    return out

# node = ListNode(1)
# bus = node
# bus.next = ListNode(2)
# bus=bus.next
# bus.next = ListNode(3)
# bus=bus.next
# bus.next = ListNode(4)

# node2 = ListNode(1)
# bus = node2
# bus.next = ListNode(2)
# bus=bus.next
# bus.next = ListNode(3)
# bus=bus.next
# bus.next = ListNode(4)
# i = mergeKLists([node])
# while i:
#     print(i.val)
#     i = i.next

def trap(height):
        a = 0
        left = 0
        right = 0
        l, r = 0, len(height)-1
        if not height: return 0
        while l<r:
            if height[l] <= height[r]:
                if height[l] > left:
                    left = height[l]
                else:
                    a += left - height[l]
                l+=1
            else:
                if height[r] > right:
                    right = height[r]
                else:
                    a += right - height[r]
                r-=1
        return a

def maxSubArray(nums):
    if not nums: return 0
    i = 0
    sumCurrent = 0
    maxSum = nums[i]
    while i<len(nums):
        if sumCurrent+nums[i]<=0:
            sumCurrent = 0
            maxSum = max(maxSum, nums[i])
        else:
            sumCurrent+=nums[i]
            maxSum = max(maxSum, sumCurrent)
        i+=1
    return maxSum

def spiralOrder(matrix):
    out = []
    while matrix:
        # RIGHT
        out += matrix.pop(0)
        if not matrix: return out
        # DOWN
        for i in matrix:
            if i!=[]:
                out.append(i.pop(-1))
        if not matrix: return out
        # LEFT
        matrix[-1].reverse()
        out += matrix.pop(-1)
        if not matrix: return out
        # UP
        for i in range(len(matrix)-1,-1,-1):
            if matrix[i]!=[]:
                out.append(matrix[i].pop(0))
    return out

m = [[1],[2],[3],[4],[5],[6],[7],[8],[9],[10]]
# m = [[1,2,3],[4,5,6],[7,8,9],[10,11,12]]
print(spiralOrder(m))

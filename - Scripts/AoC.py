f = open("Desktop/input.txt")
# sum = 0
# max = [0,0,0]
# for x in f:
#     if x=='\n':
#         if sum>max[0]:
#             max[0]=sum
#             max.sort()
#         sum=0
#     else:
#         sum+=int(x)
# if sum>max[0]:
#             max[0]=sum
#             max.sort()
# print(max[0]+max[1]+max[2])

# f = open("Desktop/input.txt")
# pts = 0
# for x in f:
#     # if(x=='\n'):break
#     if x[2] == 'X': #lose
#         if x[0] == 'A': #Rock
#             pts+=3
#         if x[0] == 'B': #Paper
#             pts+=1
#         if x[0] == 'C': #Scissors
#             pts+=2
#     if x[2] == 'Y': #draw
#         if x[0] == 'A': #Rock
#             pts+=1
#         if x[0] == 'B': #Paper
#             pts+=2
#         if x[0] == 'C': #Scissors
#             pts+=3
#         pts+=3
#     if x[2] == 'Z': #win
#         pts+=6
#         if x[0] == 'A': #Rock
#             pts+=2
#         if x[0] == 'B': #Paper
#             pts+=3
#         if x[0] == 'C': #Scissors
#             pts+=1
# print(pts)

f = open("Desktop/input.txt")
prio = 0
for x in f:
    x = x.split('\n')[0]
    if i in c2:
        if ord(i)>96:
            prio += ord(i)-96
        else:
            prio += ord(i)-38
        break
print(prio)
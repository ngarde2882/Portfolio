# def find_betweens(before, after, s):
#     result = []
#     b = len(before)
#     a = len(after)
#     i = 0
#     word = ""
#     while i<(len(s)-b):
#         if(s[i:i+b]==before):
#             i+=b
#             while i<(len(s)-a):
#                 if(s[i:i+a]==after):
#                     result.append(word)
#                     word = ""
#                     i += a
#                     break
#                 else:
#                     word+=s[i]
#                 i+=1
#         i+=1
#     return result



# stringy = "<td align=\"left\" class=\"fooinfo\" colspan=\"5\">\n<a href=\"/abilitydex/honeygather.shtml\"><b>Honey Gather</b></a>: May pick up a Honey after battle; the higher the level, the higher the chance. <br/>\n<b>Hidden Ability</b><!-- <i>(Available)</i>-->: <br/><a href=\"/abilitydex/hustle.shtml\"><b>Hustle</b></a>: Damage from physical attacks is increased by 50%, but average accuracy is only 80%. </td>"

# print(find_betweens("<b>", "</b>", stringy))


string = ['one', 'two', 'three']

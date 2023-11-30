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


# def lower(string_in):
#     if type(string_in) == list: # list
#         for i in range(len(string_in)):
#             for c in string_in[i]:
#                 string_in[i] = string_in[i].replace(c, c.lower())
#             print('s:',string_in[i])
#         print('s_i',string_in)
#         return string_in
#     elif type(string_in) == str: # string
#         for c in string_in:
#             string_in = string_in.replace(c, c.lower())
#         return string_in
#     else:
#         raise('ONLY STRINGS AND LISTS OF STRINGS CAN BE INPUT IN THIS FUNCTION')
    
# string = ['oNe', 'Two', 'thrEE']

# print(lower(string))

# import klefkeys

# import firebase_admin
# from firebase_admin import credentials
# from firebase_admin import db
# firebase_admin.initialize_app(credentials.Certificate(klefkeys.firebase_cred), {'databaseURL':klefkeys.firebase_url})

# function that checks for lowercase before an uppercase, then outputs position of uppercase
def lower_to_upper(s):
    for c in range(1, len(s)):
        if s[c] == s[c].upper():
            if s[c]=='-': return None # check against Ho-Oh and Porygon-Z that should return None
            if s[c]==' ': return None # check against Mime Jr.
            if s[c]=='.': return None # check against Mr. Mime and Mr. Rime
            if s[c-1] == s[c-1].lower():
                return c
    return None

mon = 'Mr. Mime'
i = lower_to_upper(mon)
print(mon[:i])
import re

my_r =re.compile('regex pattern')
mo = my_r.search('regex pattern lksjs regex pattern')
print(mo.group())

my_2  = re.compile(r'\d\d\d-\d\d')
m_2 = my_2.search('1234-54-hhh')
if m_2 is not  None:
    print(m_2.group())

re_3 = re.compile(r'([^aeiou][aeiou])+')
m_3 = re_3.search('hasasaga')
print(len(m_3.groups()))
for g in m_3.groups():
    print(g)
# if m_3 is not None:
#     print(m_3.group())

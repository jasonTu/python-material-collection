# coding: utf-8

str_a = '这是一段汉字'
a_content ='\xe8\xbf\x99\xe6\x98\xaf\xe4\xb8\x80\xe6\xae\xb5\xe6\xb1\x89\xe5\xad\x97'
print('str_a == a_content:', str_a == a_content)

print(str_a)
print(type(str_a))

uni_b = str_a.decode('utf-8')
b_content = u'\u8fd9\u662f\u4e00\u6bb5\u6c49\u5b57'
print('uni_b == b_content:', uni_b == b_content)
print(uni_b)
print(type(uni_b))

'''
('str_a == a_content:', True)
这是一段汉字
<type 'str'>
('uni_b == b_content:', True)
这是一段汉字
<type 'unicode'>
'''

#Python基本数据类型
##Number
Python3 支持 int、float、bool、complex（复数）
```python
a, b, c, d = 520, 520.1314, True, 1+2j
print(type(a), type(b), type(c), type(d))
```
##String
字符串是由 Unicode 码位构成的不可变 序列，字符串用单引号 ' 或双引号 " 括起来，同时使用反斜杠 \ 转义特殊字符
```python
s = 'who am i'
print(s, s.split(' ')[0], s[4:6], s[-1])
```
##List
列表是可变序列，通常用于存放同类项目的集合（其中精确的相似程度将根据应用而变化）
```python
l = ['I', 'love', 'make', 'money']
print(' '.join(l), l[1::2])
```
##Tuple
元组是不可变序列，通常用于储存异构数据的多项集（例如由 enumerate() 内置函数所产生的二元组）。 
元组也被用于需要同构数据的不可变序列的情况（例如允许存储到 set 或 dict 的实例）
```python
t = (521, 'money')
print(t[0], t[1], t*2)
```
##Set
集合是由一个或数个形态各异的大小整体组成的，构成集合的事物或对象称作元素或是成员
```python
s1, s2, s3 = {'love'}, {'peace'}, set('&')
print(s1 | s2 | s3)
```
##Dictionary
字典是一种映射类型，字典用 {} 标识，它是一个无序的 键(key) : 值(value) 的集合
```python
d = dict(韦小宝='鹿鼎公', wife_num=7)
print(d['韦小宝'], '老婆个数: {}'.format(d['wife_num']))
```


# coding: utf-8

# # クイーングラフ彩色問題

# Microsoft Researchの開発したSMT(Satisfiability modulo theories)を使ってパズルを解くことを試みる．
# まずは，z3というモジュールに含まれる定義を使うことを宣言する．

# 

# In[1]:

from __future__ import print_function
import sys
sys.path.append('/usr/lib/python2.7/dist-packages/z3')
from z3 import *


# 記述をシンプルにするためにこのようにしたが，名前空間 (name space) をシンプルにすることを意図するなら，
#  import z3
# とした上で，`z3.Var('x')` などと記述することができる．

# ### 準備
# nの初期値を設定する．また，solverを作る．

# In[2]:

print(sys.argv)
n = int(sys.argv[1])
solver = Solver()


# これで，ソルバが作られる．
# ### 変数を作る
# 解くパズルは「変数」と「制約」で表現する． 
# 「変数」としては，bool変数，整数変数などいろいろある．
# まずは， n x n のマス square[y][x] に置かれているqueenの色を変数とする．

# In[3]:

squares = [[Int('s_%d_%d' % (x, y)) for y in range(n)] for x in range(n)]


# ### 制約を書く
# まずsquaresの要素は0以上n - 1以下である．それを書く
# 

# In[4]:

for r in squares:
    for s in r:
        solver.add(0 <= s, s < n)


# 次に行ごとに重複がないことを書く．

# In[5]:

for r in squares:
    solver.add(Distinct(r))


# 何気なく python の sum などを使っているが，これが正しい制約に変換されていることは，
#  solver
# などとして，加えられた制約を表示させてみると分かる．
# 次に列ごと重複がないことを書く．

# 行ごとに0, n-1 までのいずれかの要素が存在することを加える

# In[6]:

for r in squares:
    for i in range(n):
        solver.add(Or([i == s for s in r]))


# In[7]:

for x in range(n):
    solver.add(Distinct([r[x] for r in squares]))
    for i in range(n):
        solver.add(Or([i == r[x] for r in squares]))


# 斜め同士に同じ数字の駒が存在しないという制約も書いてみよう

# In[ ]:

for d in range(-n + 2, n - 1, 1):
    r1 = [squares[x + d][x] for x in range(n) if x + d >= 0 and x + d < n]
    solver.add(Distinct(r1))
    if len(r1) == n:
        for i in range(n):
            solver.add(Or([i == s for s in r1]))
    r2 = [squares[n - 1 - x + d][x] for x in range(n) if n - 1 - x + d >= 0 and n - 1 - x + d < n]
    solver.add(Distinct(r2))
    if len(r2) == n:
        for i in range(n):
            solver.add(Or([i == s for s in r2]))


# 意味があるかどうかわからないが，最初のrowを[0 .. n-1]に限定してみる．
for i in range(n):
    solver.add(squares[0][i] == i)
# これが解を持つかどうかは `solver.check()` がsatを返すことで確認できる．

# In[ ]:

r = solver.check()
print(r)


# この時に変数にどのような割り当てが行われて制約が満たされたかは，`solver.model()` で確認できる．

# In[ ]:

if r == sat:
    print(solver.model())


# 見やすくするためクイーンの存在するところに`X`, 存在しないところに`.`を表示してみよう
# solverのmodel() で得られのは辞書 (dictionary)で，変数をキーとして割り当て結果が得られるが，
# 整数型の変数の場合は，IntNumRefなので，普通の整数にするにはas_long() で変換する必要がある．

# In[ ]:

if r == sat:
    m = solver.model()
    for r in squares:
        print(''.join('%X' % m[r[i]].as_long() for i in range(n)))


# In[ ]:

# CPU: Intel(R) Core(TM) i7-6700K 
# Memory: 32GB
# OS: Ubuntu 16.04.1 LTS
# 上で
# python2 queen_coloring1.py 12
# を実行したところ，

# real    8395m33.171s
# user    8395m38.900s
# sys     0m1.012s
# で以下の解を返した．
#
# 0123456789AB
# B8796A152430
# A054392876B1
# 86AB27490153
# 32451B0A6798
# 19607384B52A
# 73B15296A084
# 4A0698325B17
# 9587A0B14362
# 6B1284739A05
# 243A065B1879
# 5798B1A03246




# coding: utf-8

# # クイーングラフ彩色問題

# Microsoft Researchの開発したSMT(Satisfiability modulo theories)を使ってパズルを解くことを試みる．
# 
# まずは，z3というモジュールに含まれる定義を使うことを宣言する．

# 

# In[64]:

from __future__ import print_function
import sys
sys.path.append('/usr/lib/python2.7/dist-packages/z3')
from z3 import *


# 記述をシンプルにするためにこのようにしたが，名前空間 (name space) をシンプルにすることを意図するなら，
#  import z3
# とした上で，`z3.Var('x')` などと記述することができる．

# ### 準備
# nの初期値を設定する．また，solverを作る．

# In[65]:

print(sys.argv)
n = int(sys.argv[1])
solver = Solver()


# これで，ソルバが作られる．
# ### 変数を作る
# 解くパズルは「変数」と「制約」で表現する．
# 「変数」としては，bool変数，整数変数などいろいろある．まずは，
# n x n のマス `square[y][x]` に置かれているqueenの色を変数とする．

# In[66]:

squares = [[[Bool('b_%d_%d_%d' % (x, y, v)) for v in range(n)] for y in range(n)] for x in range(n)]


# ### 制約を書く
# まずsquaresの要素は0以上n - 1以下である．それを書く
# 

# 準備のために，bool変数のリストに対して，たかだか1つがtrue (atmost_one), ちょうど1つがtrue(exact_one) という制約を与える補助関数を用意する．

# In[67]:

def atmost_one(solver, l):
    for i in range(len(l)):
        for j in range(i):
            solver.add(Or(Not(l[i]), Not(l[j])))
def exact_one(solver, l):
    solver.add(Or(l))
    atmost_one(solver, l)



# すべてのマスについて，どれか一つがtrueだという条件を書く．

# In[68]:

for r in squares:
    for s in r:
        exact_one(solver, s)


# 次に行ごとに重複がなく要素が一つだけ存在することを書く．

# In[69]:

for r in squares:
    for i in range(n):
        exact_one(solver, [r[x][i] for x in range(n)])


# 列ごとに重複がないことを書く．

# In[70]:

for x in range(n):
    for i in range(n):
        exact_one(solver, [squares[y][x][i] for y in range(n)])


# 斜め同士に同じ数字の駒が存在しないという制約も書いてみよう

# In[71]:

for d in range(-n + 2, n - 1, 1):
    r1 = [squares[x + d][x] for x in range(n) if x + d >= 0 and x + d < n]
    r2 = [squares[n - 1 - x + d][x] for x in range(n) if n - 1 - x + d >= 0 and n - 1 - x + d < n]
    for i in range(n):
        if len(r1) == n:
            exact_one(solver, [s[i] for s in r1])
        else:
            atmost_one(solver, [s[i] for s in r1])
        if len(r2) == n:
            exact_one(solver, [s[i] for s in r2])
        else:
            atmost_one(solver, [s[i] for s in r2])


# 最初のrowを[0 .. n-1]に限定してみる．

# In[72]:

for i in range(n):
    solver.add(squares[0][i][i])


# これが解を持つかどうかは `solver.check()` がsatを返すことで確認できる．

# In[73]:

res = solver.check()


# この時に変数にどのような割り当てが行われて制約が満たされたかは，`solver.model()` で確認できる．

# In[74]:

if res == sat:
    solver.model()


# 見やすくするためクイーンの存在するところに`X`, 存在しないところに`.`を表示してみよう
# solverのmodel() で得られのは辞書 (dictionary)で，変数をキーとして割り当て結果が得られるが，
# 整数型の変数の場合は，IntNumRefなので，普通の整数にするにはas_long() で変換する必要がある．

# In[75]:

if res == sat:
    m = solver.model()
    for row in squares:
        print(''.join('%X' % [is_true(m[row[i][j]]) for j in range(n)].index(True) for i in range(n)))


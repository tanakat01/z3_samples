# queen_graph
- 第58回プログラミング・シンポジウム ( http://www.ipsj.or.jp/prosym/58/58program.html ) の発表
田村直之，宋剛秀，番原睦則: SATソルバーの使い方 -問題をSATに符号化する方法-, 第58回プログラミング･シンポジウム予稿集, pp. 165 - 172 (2017).
に紹介されていたクイーングラフ彩色問題を解くプログラムです．
  - queen_coloring1.py は整数でencodingしてlinear algebra をtheoryとして使ったものです．
  - queen_coloring_bool.py はboolのみを使ったもの．符号化およびヒントは，上記論文の COL+D+H2 に対応します．
- 実験環境
  - CPU: Intel(R) Core(TM) i7-6700K CPU @ 4.00GHz
  - Memory: memory 32GB
  - OS: Ubuntu 16.04.1 LTS
  - Python: Python 2.7.12
- 実行時間(user時間, 単位は秒)

|  program \ n | 5 | 6 | 7 | 8 | 9 | 10 | 11 | 12 |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| queen_coloring1.py | 0.064 | 0.084 | 0.136 | 0.280 | 19.924 | 127.548 | 4174.640 | 503678.900 |
| queen_coloring_bool.py | 0.196 | 0.392 | 0.716 | 1.212 | 2.484 | 15.880 | 282.384 | 382270.376 | 

```
 python2 queen_coloring1.py 12 
 0123456789AB
 B8796A152430
 A054392876B1
 86AB27490153
 32451B0A6798
 19607384B52A
 73B15296A084
 4A0698325B17
 9587A0B14362
 6B1284739A05
 243A065B1879
 5798B1A03246
 real    8395m33.171s
 user    8395m38.900s
 sys     0m1.012s
--------
 python2 queen_coloring_bool.py 12 
0123456789AB
489A6B051237
A6703928B451
758120B9A364
3B459A126708
1237065B489A
9AB687435012
B354129A7680
6409A8312B75
2768B1A03549
501273849AB6
89AB54760123

real    6371m3.264s
user    6371m10.376s
sys     0m0.852s
```



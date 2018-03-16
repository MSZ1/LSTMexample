#!/usr/bin/env python
# -*- coding: utf-8 -*-
import codecs
from MeCab import Tagger
from pyknp import Juman
text=""
f=codecs.open('pyro.txt', 'r', 'utf-8')
fin=codecs.open('mecab.txt','a','utf-8')
fin1=codecs.open('juman.txt','a','utf-8')
m = Tagger("-Owakati")
juman = Juman()
for line in f:
    target_text=line
    inp=m.parse(target_text)
    fin.write(inp)
    #result = juman.analysis(target_text)
    #inp1=(' '.join([mrph.midasi for mrph in result.mrph_list()]))
    #fin1.write(inp1)
print("終了")
f.close()

##juman++で実行すると途中で書式のエラーが発生した(コーディングを変えればOK…かな？)
##したがって扱うテキストファイルはmecabのものとする
##同じディレクトリにnuc.zipを解凍したものを配置すれば実行できる

#!/usr/bin/env python
# @Date    : 2017-05-02 14:00:03
# @Author  : spring (spring_chu@sjtu.edu.cn)
# @Link    : ${link}
# @Version : $Id$
from sentiment import sentiment_score
import re

str = "https://www.incd.cdnqqq @today @spring is #raining,I do not love it.https://www.incd.cdn"
print str
print sentiment_score(str)
remove_http = re.compile(r'https://[a-zA-Z0-9.?/&=:]*', re.S)
remove_s = re.compile(r'@[a-zA-Z0-9.?/&=:]*', re.S)
dd = remove_http.sub("", str)
print dd
print sentiment_score(dd)
ss = remove_s.sub("", dd)
print ss
print sentiment_score(ss)
print sentiment_score("gaoxiao!!!")

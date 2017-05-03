#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Date    : 2017-05-02 14:00:03
# @Author  : spring (spring_chu@sjtu.edu.cn)
# @Link    : ${link}
# @Version : $Id$
from sentiment import sentiment_score

str="today is raining,I do not love it.@spring  #raining https://asdas/sadas.cn"
print sentiment_score(str)
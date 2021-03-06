#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Date    : 2017-04-08 18:03:31
# @Author  : spring (spring_chu@sjtu.edu.cn)
# @Link    : ${link}
# @Version : $Id$

import os
from mysql import MySQL
import datetime
import time
from sentiment import sentiment_score
import re
# 远程主机
conn = MySQL()
conn.selectDb('twitter')

# 本地主机
#myhost = "107.191.118.80"
myhost = "127.0.0.1"
myuser = "root"
mypw = ""
myconn = MySQL(myhost, myuser, mypw)
myconn.selectDb('twitter')

'''
# 获取popularity相关数据
# retweet数目和favorite数目
# 要求每隔1个小时得一个数据
# 按照status_id,updataTime,count 增序查询（注意不能在字段上加'',这样查询无效）
sql_get_stauts = "select distinct * from statusupdate2 order by status_id,updateTime,count asc"
results_1 = conn.query(sql_get_stauts)
print u"查询条数：" + str(results_1)
res_status_1 = conn.fetchAll()
for row in res_status_1:
    status_id_1 = row['status_id']
    retweet_1 = row['retweet_count']
    favorite_1 = row['favorite_count']
    pretime = row['updateTime']
    # caculate the time
    #date1 = datetime.datetime.now()
    sql_time = "select * from status where status_id='%s'" % (status_id_1)
    check_time = myconn.query(sql_time)
    print "check_time:" + str(check_time)
    if check_time > 0:
        res_time = myconn.fetchRow()
        catchtime = res_time[5]
        print "catch_time:" + str(catchtime)
        date1 = datetime.datetime.strptime(
            str(catchtime), "%Y-%m-%d %H:%M:%S")
    else:
        date1 = datetime.datetime.strptime(str(pretime), "%Y-%m-%d %H:%M:%S")
    date2 = datetime.datetime.strptime(str(pretime), "%Y-%m-%d %H:%M:%S")
    tdate = date2 - date1
    update_time = int(round((tdate.days * 24 * 3600 + tdate.seconds) / 3600))
    print "updatetime:" + str(update_time)
    print "status:" + status_id_1
    print "retweet:" + retweet_1
    print "favorite:" + favorite_1
    for utime in range(update_time):
        sql_check_1 = "select * from popularity where status_id='%s' and pretime='%d'" % (
            status_id_1, utime)
        check_1 = myconn.query(sql_check_1)
        # 如果重复不更新
        #res_1 = myconn.fetchAll()
        # for i in res_1:
        #    myretweet_1 = i['retweet']
        #    myfavorite_1 = i['favorite']

        if check_1 > 0:
            print "数据已存在"
            # if int(retweet_1) > int(myretweet_1) or int(myfavorite_1) > int(favorite_1):
            # sql_up_1 = "update popularity set retweet = '%s',favorite ='%s' where status_id ='%s' and pretime='%d'" % (
            # myretweet_1, myfavorite_1, status_id_1, update_time)
            # try:
            # myconn.query(sql_up_1)
            # myconn.commit()
            # print sql_up_1 + "success"
            # except:
            # myconn.rollback()
            # print sql_up_1 + "fail"
        else:
            sql_ins_1 = "insert into popularity(status_id,pretime,retweet,favorite) values('%s','%s','%s','%s')" % (
                status_id_1, utime, retweet_1, favorite_1)
            try:
                myconn.query(sql_ins_1)
                myconn.commit()
                print sql_ins_1 + "success"
            except:
                myconn.rollback()
                print sql_ins_1 + "fail"

print "set popularity finished"
'''

# imitator 模仿因子，获取tweet文本的信息
# status_id, characters数目,createtime,
sql_status = "select distinct * from status"
results_2 = conn.query(sql_status)
print u"查询条数:" + str(results_2)
res_stauts_2 = conn.fetchAll()
for row in res_stauts_2:
    status_id_2 = row['status_id']
    user_id_2 = row['user_id']
    characters = len(row['text'])
    ctime = row['created_at']
    context = row['text']
    url = context.count("https")
    hashtag = context.count("#")
    atuser = context.count("@")
    remove_http = re.compile(r'https://[a-zA-Z0-9.?/&=:]*', re.S)
    remove_s = re.compile(r'@[a-zA-Z0-9.?/&=:]*', re.S)
    context_rh = remove_http.sub("", context)
    context_pre = remove_s.sub("", context_rh)
    sentiment = sentiment_score(context_pre)
    # caculate the time
    date1 = datetime.datetime.now()
    date2 = datetime.datetime.strptime(str(ctime), "%Y-%m-%d %H:%M:%S")
    tdate = date1 - date2
    create_time = int(round((tdate.days * 24 * 3600 + tdate.seconds) / 3600))
    print "status_id:" + status_id_2
    print "user_id:" + user_id_2
    print "characters:" + str(characters)
    print "timenow:" + str(datetime.datetime.now())
    print "time:" + str(ctime)
    print "timehour:" + str(create_time)
    print "text:" + row['text']
    print "hashtag:" + str(hashtag)
    print "url:" + str(url)
    print "atuser:" + str(atuser)
    print "After precontext:" + context_pre
    print "sentiment:" + str(sentiment)
    sql_check = "select * from imitator where user_id='%s' and status_id='%s'" % (
        status_id_2, status_id_2)
    check = myconn.query(sql_check)
    print "check:" + str(check)
    if check > 0:
        sql_up = "update imitator set hashtag='%d',url='%d',atuser='%d',sentiment='%s' characters='%d', create_time='%d',context='%s' where status_id='%s' and user_id='%s'" % (
            hashtag, url, atuser, sentiment, characters, create_time, context_pre, status_id_2, user_id_2)
        try:
            myconn.query(sql_up)
            myconn.commit()
            print sql_up + "success"
        except:
            myconn.rollback()
            print sql_up + "fail"
    else:
        sql_ins = "insert into imitator(status_id,user_id,hashtag,url,atuser,sentiment,characters,create_time,context) values('%s','%s','%d','%d','%d','%s','%d','%d','%s')" % (
            status_id_2, user_id_2, hashtag, url, atuser, sentiment, characters, create_time, context_pre)
        try:
            myconn.query(sql_ins)
            myconn.commit()
            print sql_ins + "success"
        except:
            myconn.rollback()
            print sql_ins + "fail"
print "set imitator finished"

'''
# innovator 创新因子，存储user本身特性的属性
# status_id user_id twitter数目  follower数目 friends数目
sql_user_3 = "select distinct * from users order by 'created_at' desc"
results_3 = conn.query(sql_user_3)
print u"查询条数：" + str(results_3)
res_stauts_3 = conn.fetchAll()
for row in res_stauts_3:
    user_id_3 = row['user_id']
    friends = row['friends_count']
    follower = row['followers_count']
    twitter = row['statuses_count']
    favorite = row['favourites_count']
    sql_following = "select * from follower where follower_id='%s'" % (
        user_id_3)
    res_3 = conn.query(sql_following)
    if res_3 > 0:
        following = res_3
    else:
        following = 0
    print "user_id:" + user_id_3
    print "friends:" + friends
    print "follower:" + follower
    print "twitter:" + twitter
    print "favorite:" + favorite
    print "following:" + str(following)
    sql_check_3 = "select * from innovator where user_id='%s'" % (user_id_3)
    check_3 = myconn.query(sql_check_3)
    if check_3 > 0:
        sql_up = "update innovator set friends='%s', follower='%s',twitter='%s',favorite='%s',following='%s' where user_id='%s'" % (
            friends, follower, twitter, favorite, following, user_id_3)
        try:
            myconn.query(sql_up)
            myconn.commit()
            print sql_up + "success"
        except:
            myconn.rollback()
            print sql_up + "fail"
    else:
        sql_ins = "insert into innovator(user_id,friends,follower,twitter,favorite,following) values('%s','%s','%s','%s','%s','%s')" % (
            user_id_3, friends, follower, twitter, favorite, following)
        try:
            myconn.query(sql_ins)
            myconn.commit()
            print sql_ins + "success"
        except:
            myconn.rollback()
            print sql_ins + "fail"
print "set innovator finished"
'''
# conn.close()
# myconn.close()

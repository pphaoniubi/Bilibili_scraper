import requests
import os
import time
import random


def bv2av(v_aid):
    """"""


def CommentScraper(max_page):


    for i in range(max_page):
        print('page ' + str(i))
        time.sleep(random.uniform(0,1))         #wait randomly to avoid being detected
        url = 'https://api.bilibili.com/x/v2/reply?&jsonp=jsonp&pn={}&type=1&oid={}&sort=2'.format(i ,'531176482')

        response = requests.get(url=url)

        print(response)

        #create storing data list
        message_list = []
        IP_list = []
        sex_list = []
        time_list = []
        like_list = []

        reply = response.json()['data']['replies']
        for r in reply:
            #message
            message = r['content']['message']
            
            try:
                #main reply IP
                IP = r['reply_control']['location']         #maybe set it to unknow when it's not found?
            except:
                IP = ''

            #sex
            sex = r['member']['sex']

            #reply ctime
            r_time = r['ctime']


            #reply likes
            like = r['like']

            #sub-replies info
            sub_reply = r['replies']
           
            if sub_reply is not None:
                for sub_r in sub_reply:
                    #sub_reply_sex
                    sub_sex = sub_r['member']['sex']

                    #sub_reply IP
                    try:
                        sub_IP = sub_r['member']['reply_control']['location']

                    except:
                        sub_IP = ''      

                    


CommentScraper(5)

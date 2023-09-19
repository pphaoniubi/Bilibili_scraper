import requests
import os
import time
import random
import pandas as pd
from datetime import datetime




def bv2av(bid):
    """"""


def RemoveFile():
    if os.path.exists(outfile):
        os.remove(outfile)


def CommentScraper(max_page, aid):
        
    try:
        headers = {
            'cookie': "_uuid=E49ECC210-39810-BE10B-6C95-3A9D4D58861371617infoc; buvid3=883FC05C-7475-B4D7-2525-AFAFEAC4044673245infoc; b_nut=1664753373; i-wanna-go-back=-1; b_ut=7; nostalgia_conf=-1; CURRENT_FNVAL=4048; rpdid=|(JJlu|~kJRl0J'uYmkR|~RkY; SESSDATA=07488c42%2C1707959605%2C964ee%2A81VfvYAXv18YIGcA0Tu71XMpU-8j7i1k75Q9L0pPVd4Gk1Gk9qAqu2vhqKr6zVaXsoSdmp-gAALAA; bili_jct=d3fa3517fdc7c9b050815ab073012bae; DedeUserID=386411344; DedeUserID__ckMd5=64519e7af412cb8f; sid=6c9bsdi3; header_theme_version=CLOSE; home_feed_column=5; fingerprint=d846ee59e8071a67f909f0060aba3a8b; buvid_fp_plain=undefined; buvid_fp=d846ee59e8071a67f909f0060aba3a8b; buvid4=A9AA6B41-E06D-F599-2121-6057BEC4BBD673245-022100307-PMg%2Bj%2FKYHNqGxLEcltkmCg%3D%3D; b_lsid=289EBE34_18AA90AA205; browser_resolution=1680-908; bili_ticket=eyJhbGciOiJIUzI1NiIsImtpZCI6InMwMyIsInR5cCI6IkpXVCJ9.eyJleHAiOjE2OTUzMTI0NTMsImlhdCI6MTY5NTA1MzI1MywicGx0IjotMX0.T67Y9-uEcICieqypISVLiK5Utgfb8lh5FIYk9g05_5I; bili_ticket_expires=1695312453; PVID=1; bp_video_offset_386411344=841537427947388960; bsource=search_google",

        }

        for i in range(max_page):

            message_list = []
            IP_list = []
            sex_list = []
            time_list = []
            like_list = []
            is_main = []

            print('page ' + str(i))
            time.sleep(random.uniform(0,1))         #wait randomly to avoid being detected
            url = 'https://api.bilibili.com/x/v2/reply?&jsonp=jsonp&pn={}&type=1&oid={}&sort=2'.format(i , aid)

            response = requests.get(url=url, headers=headers)

            print(response)
            print(url)
            #create storing data list

            reply = response.json()['data']['replies']

            for r in reply:
                #message
                message = r['content']['message']
                message_list.append(message)
                try:
                    #main reply IP
                    IP_region = r['reply_control']['location']         #maybe set it to unknow when it's not found?
                except Exception as e:
                    IP_region = ''
                    print(e)
                    print(r['reply_control'])
                IP_list.append(IP_region.replace('IP属地：', ''))

                #sex
                sex = r['member']['sex']
                sex_list.append(sex)

                #reply ctime
                r_time = r['ctime']
                time_list.append(datetime.fromtimestamp(r_time))

                #reply likes
                like = r['like']
                like_list.append(like)
                
                is_main.append('True')
                

                #sub-replies info
                sub_reply = r['replies']

                
                if sub_reply is not None:
                    for sub_r in sub_reply:
                        #sub_reply_sex
                        sub_sex = sub_r['member']['sex']
                        sex_list.append(sub_sex)
                        #sub_reply IP
                        try:
                            sub_IP = sub_r['reply_control']['location']
                        except:
                            sub_IP = ''
                        IP_list.append(sub_IP.replace('IP属地：', ''))

                        sub_like = sub_r['like']
                        like_list.append(sub_like)

                        sub_content = sub_r['content']['message']
                        message_list.append(sub_content)

                        sub_ctime = sub_r['ctime']
                        time_list.append(datetime.fromtimestamp(sub_ctime))

                        is_main.append('False')

            df = pd.DataFrame({
                '评论页码': i + 1,
                'IP属地': IP_list,
                '性别': sex_list,
                '评论时间': time_list,
                '点赞数': like_list,
                '主评论': is_main,
            })

            if os.path.exists(outfile):
                header = False
            else:
                header=True

            df.to_csv(outfile, mode = 'a+', encoding = 'utf_8_sig', index = False, header = header)

    except Exception as e:
        print('error taking place in video: {}'.format(aid))


def getAidBySearchKeyword(keyword):
    headers = {
        'cookie': "_uuid=E49ECC210-39810-BE10B-6C95-3A9D4D58861371617infoc; buvid3=883FC05C-7475-B4D7-2525-AFAFEAC4044673245infoc; b_nut=1664753373; i-wanna-go-back=-1; b_ut=7; nostalgia_conf=-1; CURRENT_FNVAL=4048; rpdid=|(JJlu|~kJRl0J'uYmkR|~RkY; SESSDATA=07488c42%2C1707959605%2C964ee%2A81VfvYAXv18YIGcA0Tu71XMpU-8j7i1k75Q9L0pPVd4Gk1Gk9qAqu2vhqKr6zVaXsoSdmp-gAALAA; bili_jct=d3fa3517fdc7c9b050815ab073012bae; DedeUserID=386411344; DedeUserID__ckMd5=64519e7af412cb8f; sid=6c9bsdi3; header_theme_version=CLOSE; home_feed_column=5; fingerprint=d846ee59e8071a67f909f0060aba3a8b; buvid_fp_plain=undefined; buvid_fp=d846ee59e8071a67f909f0060aba3a8b; buvid4=A9AA6B41-E06D-F599-2121-6057BEC4BBD673245-022100307-PMg%2Bj%2FKYHNqGxLEcltkmCg%3D%3D; b_lsid=289EBE34_18AA90AA205; browser_resolution=1680-908; bili_ticket=eyJhbGciOiJIUzI1NiIsImtpZCI6InMwMyIsInR5cCI6IkpXVCJ9.eyJleHAiOjE2OTUzMTI0NTMsImlhdCI6MTY5NTA1MzI1MywicGx0IjotMX0.T67Y9-uEcICieqypISVLiK5Utgfb8lh5FIYk9g05_5I; bili_ticket_expires=1695312453; PVID=1; bp_video_offset_386411344=841537427947388960; bsource=search_google",
    }

    url = 'https://api.bilibili.com/x/web-interface/search/all/v2?page=1&keyword={}'.format(keyword)

    response = requests.get(url, headers=headers)

    video_list = response.json()['data']['result'][11]['data']

    aid_list = []

    for video in video_list:

        if video['video_review'] > 10000:
            aid_list.append(video['aid'])

    return aid_list



if __name__ == '__main__':

    
    
    outfile = 'bilibili.csv'
    #if file exists, remove
    RemoveFile()
    

    for aid in getAidBySearchKeyword('tf boys'):
        CommentScraper(500, aid)
import requests
import os
import time
import random
import pandas as pd
from datetime import datetime
from pathlib import Path



def bv2av(bv):

    Str = 'fZodR9XQDSUm21yCkr6zBqiveYah8bt4xsWpHnJE7jL5VG3guMTKNPAwcF'
    Dict = {}

    for i in range(58):
        Dict[Str[i]] = i

    s = [11, 10, 3, 8, 4, 6, 2, 9, 5, 7]

    xor = 177451812
    add = 100618342136696320

    if bv.find('BV') == -1:
        bv = 'BV' + bv

    r = 0
    for i in range(10):
        r += Dict[bv[s[i]]] * 58 ** i 

    
    aid = str((r - add) ^ xor)
    return aid


def CommentScraper(max_page, aid, not_200_count):
        
    try:
        headers = {
            'cookie': "buvid3=09397691-5EF8-4E68-AADA-3B6C5A07761E95551infoc; b_nut=1695443895; i-wanna-go-back=-1; b_ut=7; _uuid=9210C1B94-62AE-CAF9-6A88-13F1D2365FD1095659infoc; rpdid=|(uuul)luJ|~0J'uYmlRRJmuJ; CURRENT_QUALITY=80; header_theme_version=CLOSE; buvid4=00D6E1BD-A864-F4D3-2DE3-144055B9DF2C35615-023090402-YPxCscKgwWAVEdO1g%2BwBLA%3D%3D; buvid_fp_plain=undefined; CURRENT_FNVAL=4048; enable_web_push=DISABLE; bp_video_offset_386411344=854848068439244839; fingerprint=7e03fc6d0218c9889f67ca92295e08a0; buvid_fp=7e03fc6d0218c9889f67ca92295e08a0; home_feed_column=5; bili_ticket=eyJhbGciOiJIUzI1NiIsImtpZCI6InMwMyIsInR5cCI6IkpXVCJ9.eyJleHAiOjE2OTkzMjMwNTAsImlhdCI6MTY5OTA2Mzc5MCwicGx0IjotMX0.3fcR5n-lZSDQeEGRY4lBiLleRzNG8Qjj5Mf1zH2P_zk; bili_ticket_expires=1699322990; SESSDATA=5ba2a029%2C1714615886%2C54771%2Ab1CjB2bPU06YLQ_lJsDIoqYFcPoSzXImJDfffhAun0djRutgUFLBFL-ysSoWDcR-3YiuMSVl9JTlFKc2VMZ0JFM0U3MnRNa042SDZZMGRxc2p6NGNiLVQ2T1FucW5GZTFLMTFhaHdyUTVTOTh4ZGRlZ196U1hLb2JFWjI2cGJ6ekppWWZmQmZVbzdBIIEC; bili_jct=626631467a6dec1b614ab10ec6ef1af3; DedeUserID=3546572270864807; DedeUserID__ckMd5=d2297fde3473dfcd; sid=4gp79oof; bp_video_offset_3546572270864807=860377941931982964; browser_resolution=1498-927; b_lsid=9104E9D19_18BA212001F; PVID=3",
        }

        for i in range(max_page):

            message_list = []
            IP_list = []
            sex_list = []
            time_list = []
            like_list = []
            is_main = []

            time.sleep(random.uniform(0,0.7))         
            url = 'https://api.bilibili.com/x/v2/reply?&jsonp=jsonp&pn={}&type=1&oid={}&sort=2'.format(i , aid)

            response = requests.get(url=url, headers=headers)
            
            #create storing data list

            reply = response.json()['data']['replies']

            if reply is None or len(reply) == 0:
                print('end of comment')
                break

            print('{} page {} comments {} at aid {}'.format(response ,i + 1, len(reply), aid))

            for r in reply:
                #message
                message = r['content']['message']
                message_list.append(message)
                try:
                    #main reply IP
                    IP_region = r['reply_control']['location']         #maybe set it to unknow when it's not found?
                except Exception as e:
                    IP_region = ''
                IP_list.append(IP_region.replace('IP属地：', ''))
                
                if IP_list is None:
                    print("IP addr does not exist")

                #sex
                sex = r['member']['sex']
                sex_list.append(sex.replace('保密', ''))

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
                        sex_list.append(sub_sex.replace('保密', ''))
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
                '评论内容': message_list,
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
        print(e)
        if response.status_code != 200:
                not_200_count = not_200_count + 1

def getAidBySearchKeyword(keyword):
    create_folder_file(keyword)
    headers = {
        'cookie': "_uuid=E49ECC210-39810-BE10B-6C95-3A9D4D58861371617infoc; buvid3=883FC05C-7475-B4D7-2525-AFAFEAC4044673245infoc; b_nut=1664753373; i-wanna-go-back=-1; b_ut=7; nostalgia_conf=-1; CURRENT_FNVAL=4048; rpdid=|(JJlu|~kJRl0J'uYmkR|~RkY; SESSDATA=07488c42%2C1707959605%2C964ee%2A81VfvYAXv18YIGcA0Tu71XMpU-8j7i1k75Q9L0pPVd4Gk1Gk9qAqu2vhqKr6zVaXsoSdmp-gAALAA; bili_jct=d3fa3517fdc7c9b050815ab073012bae; DedeUserID=386411344; DedeUserID__ckMd5=64519e7af412cb8f; sid=6c9bsdi3; header_theme_version=CLOSE; home_feed_column=5; fingerprint=d846ee59e8071a67f909f0060aba3a8b; buvid_fp_plain=undefined; buvid_fp=d846ee59e8071a67f909f0060aba3a8b; buvid4=A9AA6B41-E06D-F599-2121-6057BEC4BBD673245-022100307-PMg%2Bj%2FKYHNqGxLEcltkmCg%3D%3D; b_lsid=289EBE34_18AA90AA205; browser_resolution=1680-908; bili_ticket=eyJhbGciOiJIUzI1NiIsImtpZCI6InMwMyIsInR5cCI6IkpXVCJ9.eyJleHAiOjE2OTUzMTI0NTMsImlhdCI6MTY5NTA1MzI1MywicGx0IjotMX0.T67Y9-uEcICieqypISVLiK5Utgfb8lh5FIYk9g05_5I; bili_ticket_expires=1695312453; PVID=1; bp_video_offset_386411344=841537427947388960; bsource=search_google",
        'user-agent' : 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/117.0.0.0 Safari/537.36',
    }

    url = 'https://api.bilibili.com/x/web-interface/search/all/v2?page=1&keyword={}'.format(keyword)

    response = requests.get(url, headers=headers)

    video_list = response.json()['data']['result'][11]['data']

    aid_list = []

    for video in video_list:
        aid_list.append(video['aid'])

    return aid_list


"""
get_up_main_page_vids

模式1：最新发布     pubdate
模式2：最多播放     click

"""
def get_up_main_page_vids(uid, order, max_page):
    print('getting up pig main page video aid list')


    headers = {
        'cookie' : "buvid3=09397691-5EF8-4E68-AADA-3B6C5A07761E95551infoc; b_nut=1695443895; i-wanna-go-back=-1; b_ut=7; _uuid=9210C1B94-62AE-CAF9-6A88-13F1D2365FD1095659infoc; buvid_fp=e1d49a94d93bd51e7b7a2cf02039fc66; home_feed_column=5; buvid4=00D6E1BD-A864-F4D3-2DE3-144055B9DF2C35615-023090402-YPxCscKgwWAVEdO1g+wBLA%3D%3D; CURRENT_FNVAL=4048; rpdid=|(uuul)luJ|~0J'uYmlRRJmuJ; bili_ticket=eyJhbGciOiJIUzI1NiIsImtpZCI6InMwMyIsInR5cCI6IkpXVCJ9.eyJleHAiOjE2OTU3MDMxMTUsImlhdCI6MTY5NTQ0Mzg1NSwicGx0IjotMX0.cgUA08z29O7R_hh99RbR--D6Z62hNpGQXF8abfd0iQE; bili_ticket_expires=1695703055; CURRENT_QUALITY=80; DedeUserID=386411344; DedeUserID__ckMd5=64519e7af412cb8f; SESSDATA=f3b0064d%2C1710996455%2C28418%2A91CjAigqaI88fpZnRUc80sWfpYZ4S3lvYxnQvJsq0rgrF5e2naCmB0hmfmgEcnBu4DmDUSVkJULTA0WElpMmRXcDFuNnRzTWcybjNhOGpiMXpBekJkdG51NXVBNG9WR3hXNmUzMXVGSUo4OXVzci1kQXY2WEo2VnBUSl9RdDBqUTRUSVVzby1NeE5BIIEC; bili_jct=fbdefa1b4e0f914ec2d0ac7251cb4c87; header_theme_version=CLOSE; PVID=2; browser_resolution=1556-889; bp_video_offset_386411344=844469031123550241; sid=4h5gmcc3; b_lsid=BDA391B3_18AC410BA1F; bsource=search_google",
        'user-agent' : 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/117.0.0.0 Safari/537.36'
    }

    aid_list = []
    for i in range(max_page):
        try:
            url = 'https://api.bilibili.com/x/space/wbi/arc/search?mid={}&pn={}&ps=25&index=1&order={}'.format(uid, i+1, order)      #pubdate or click

            response = requests.get(url=url, headers=headers)
            print(response)


            video_list = response.json()['data']['list']['vlist']

            if video_list is None or len(video_list) == 0:
                print('end of up main page vid_aid_list')
                break

            for aid in video_list:
                aid_list.append(aid['aid'])

        except Exception as e:
            print('error while fetching UP_main_page aid, page: {}, continue...'.format(i+1))
            print(e)    

    return aid_list

def get_up_fans(uid, max_page, outfile):
    headers = {
        'cookie' : "buvid3=09397691-5EF8-4E68-AADA-3B6C5A07761E95551infoc; b_nut=1695443895; i-wanna-go-back=-1; b_ut=7; _uuid=9210C1B94-62AE-CAF9-6A88-13F1D2365FD1095659infoc; rpdid=|(uuul)luJ|~0J'uYmlRRJmuJ; CURRENT_QUALITY=80; DedeUserID=386411344; DedeUserID__ckMd5=64519e7af412cb8f; SESSDATA=f3b0064d%2C1710996455%2C28418%2A91CjAigqaI88fpZnRUc80sWfpYZ4S3lvYxnQvJsq0rgrF5e2naCmB0hmfmgEcnBu4DmDUSVkJULTA0WElpMmRXcDFuNnRzTWcybjNhOGpiMXpBekJkdG51NXVBNG9WR3hXNmUzMXVGSUo4OXVzci1kQXY2WEo2VnBUSl9RdDBqUTRUSVVzby1NeE5BIIEC; bili_jct=fbdefa1b4e0f914ec2d0ac7251cb4c87; header_theme_version=CLOSE; buvid4=00D6E1BD-A864-F4D3-2DE3-144055B9DF2C35615-023090402-YPxCscKgwWAVEdO1g%2BwBLA%3D%3D; fingerprint=e1d49a94d93bd51e7b7a2cf02039fc66; buvid_fp_plain=undefined; buvid_fp=e1d49a94d93bd51e7b7a2cf02039fc66; CURRENT_FNVAL=4048; enable_web_push=DISABLE; home_feed_column=5; bp_video_offset_386411344=854848068439244839; PVID=4; b_lsid=D732EFF10_18B57B4A07A; browser_resolution=1484-872; sid=7phk94c0; bili_ticket=eyJhbGciOiJIUzI1NiIsImtpZCI6InMwMyIsInR5cCI6IkpXVCJ9.eyJleHAiOjE2OTgyNDI3NjYsImlhdCI6MTY5Nzk4MzUwNiwicGx0IjotMX0.FhbdAFFZ1S-vlcRwMxV4-DHobNrsJRWQ3QaHvBAtlXA; bili_ticket_expires=1698242706",
        'user-agent' : 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/117.0.0.0 Safari/537.36'
    }
    time_list = []
    for i in range(max_page):

        time.sleep(random.uniform(0,0.5)) 
        
        url = "https://api.bilibili.com/x/relation/fans?vmid={}&pn={}&ps=20&order=desc&gaia_source=main_web&web_location=333.999&w_rid=55155342fffdf15cadf76cad7110f5bf&wts=1697987324".format(uid,i)

        response = requests.get(url=url, headers=headers)

        data = response.json()['data']['list']

        print('page: {} # of fans: {} response: {}'.format(i+1, len(data),response.status_code))
        for fan in data:
            time_list.append(datetime.fromtimestamp(fan['mtime']))

        df = pd.DataFrame({
                '时间': time_list,
            })

        if os.path.exists(outfile):
            header = False
        else:
            header=True


        df.to_csv(outfile, mode = 'a+', encoding = 'utf_8_sig', index = False, header = header)

def create_folder_file(name):
    Path(name).mkdir()
    outfile = '{}/{}.csv'.format(name,name)
    if os.path.exists(outfile):
        os.remove(outfile)

    return outfile




folder_name = 'BV1ru4y147fkc'
if __name__ == '__main__':
    start_time = datetime.now()
    outfile = create_folder_file(folder_name)
    not_200_count = 0
    
    """
    aid_list = get_up_main_page_vids('207702731', 'click', 20)
    for aid in aid_list:
        print('{} video in total of {} videos'.format((aid_list.index(aid) + 1),len(aid_list)))
        CommentScraper(10000, aid, not_200_count)
    """
   
    CommentScraper(10000, bv2av(folder_name), not_200_count)

    #get_up_fans('111082383', 1000000, "马林思维粉丝")

    end_time = datetime.now()
    duration = end_time-start_time
    print('total time spent {}'.format(duration))
    print('Response failed: ')
    print(not_200_count)
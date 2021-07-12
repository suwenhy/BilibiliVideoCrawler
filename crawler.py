import requests
import os
import re
from lxml import etree


def main():
    #目标视频的url
    url_ = 'https://www.bilibili.com/video/BV1ch411h7uw'

    # 构造请求头这里的cookies
    header_ = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36',
        #'cookie': 加上cookie后可爬取会员视频
        'Referer': "https://www.bilibili.com/"
    }
    # 发送请求
    response_ = requests.get(url_, headers=header_)
    data_ = response_.text
    # 网页类型转换并获取视频名称
    html_obj = etree.HTML(data_)
    title_name = html_obj.xpath('//title/text()')[0]
    title_name = re.findall(r'(.*?)_哔哩哔哩', title_name)[0]
    print(title_name)
    # 从网页文件中提取纯视频url
    url_str = html_obj.xpath('//script[contains(text(),"window.__playinfo__")]/text()')[0]
    video_url = re.findall(r'"video":\[{"id":\d+,"baseUrl":"(.*?)",', url_str)[0]
    audio_url = re.findall(r'"audio":\[{"id":\d+,"baseUrl":"(.*?)",', url_str)[0]
    # 访问对应视频音频资源
    # 重新构建header，更改referer
    header_ = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36',
        'cookie': "_uuid=9769B430-4400-2B36-1D38-BAA4AF63644F71784infoc; buvid3=80E72A5E-DD62-4084-9CB6-F9A9B5EEAF7A34760infoc; buvid_fp=80E72A5E-DD62-4084-9CB6-F9A9B5EEAF7A34760infoc; buvid_fp_plain=80E72A5E-DD62-4084-9CB6-F9A9B5EEAF7A34760infoc; DedeUserID=32068001; DedeUserID__ckMd5=d8c39bf11dd6b44b; CURRENT_FNVAL=80; blackside_state=1; rpdid=|(u)YR|umm~l0J'uYk|u|u~lk; fingerprint3=76e3ebcbc91da698bb73b5de64176080; fingerprint_s=716e4fa81aed480a7372c286ce7c3346; SESSDATA=4de1a70e,1636891574,8ede3*51; bili_jct=34247f1ef15405c4dc61e53de7ffa2e1; sid=50ae192u; CURRENT_QUALITY=80; fingerprint=b7b05285127490faf43e75d05fb06c73; LIVE_BUVID=AUTO4316256435274370; PVID=3",
        'Referer': url_
    }
    video_data = requests.get(video_url, headers=header_).content
    audio_data = requests.get(audio_url, headers=header_).content
    title_temp = title_name + "_temp"
    #保存文件到本地
    with open (f'{title_temp}.mp4','wb')as f:
        f.write(video_data)
    with open (f'{title_temp}.mp3','wb')as f:
        f.write(audio_data)
    #合并音频和视频文件
    os.system(f'ffmpeg -i "{title_temp}.mp4" -i "{title_temp}.mp3" -c copy "{title_name}.mp4" ')
    #移除两个temp文件
    os.remove(f'{title_temp}.mp4')
    os.remove(f'{title_temp}.mp3')
main()

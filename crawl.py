import re
import json
import os
import requests
from time import sleep
from lxml import etree
import pprint
import subprocess

# 清理文件名的函数，移除非法字符
def clean_filename(filename):
    # 只保留字母、数字、下划线和点号
    return re.sub(r'[^\w\-_\.]', '_', filename)

# 合并音频和视频的函数
def merge_audio_video(video_file, audio_file, output_file):
    command = [
        'ffmpeg', '-i', video_file, '-i', audio_file, '-c:v', 'copy', '-c:a', 'aac', '-strict', 'experimental', output_file
    ]
    print(f"合并命令: {' '.join(command)}")
    try:
        result = subprocess.run(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        print("stdout:", result.stdout.decode())
        print("stderr:", result.stderr.decode())
        if result.returncode == 0:
            print(f"视频和音频已成功合并到 {output_file}")
        else:
            print("合并过程中发生错误")
    except subprocess.CalledProcessError as e:
        print(f"合并时发生错误: {e}")

# 爬取和处理单个URL的函数
def process_bilibili_url(url, headers):
    response = requests.get(url, headers=headers)
    sleep(2)
    page_text = response.text

    tree = etree.HTML(page_text)

    # 提取标题
    titles = tree.xpath('//title/text()')
    if titles:
        title = titles[0].split('_')[0].strip()  # 只取主要标题部分
        print(f"获取到的标题: {title}")
    else:
        print("无法找到标题")
        title = "Unknown Title"

    # 清理标题，生成合法的文件名
    safe_title = clean_filename(title)

    # 提取播放信息
    play_info_scripts = tree.xpath('/html/head/script[contains(text(), "window.__playinfo__")]/text()')
    if play_info_scripts:
        play_info = play_info_scripts[0][20:]  # 去掉前缀
        play_info_json = json.loads(play_info)
        pprint.pprint(play_info_json)
    else:
        print("无法找到播放信息脚本")
        play_info_json = None

    # 下载视频和音频
    if play_info_json:
        try:
            video_url = play_info_json['data']['dash']['video'][0]['baseUrl']
            audio_url = play_info_json['data']['dash']['audio'][0]['baseUrl']

            # 下载视频和音频
            video_content = requests.get(url=video_url, headers=headers).content
            audio_content = requests.get(url=audio_url, headers=headers).content

            # 创建保存目录
            if not os.path.exists('./biliVideo'):
                os.mkdir('./biliVideo')

            # 使用安全的文件名保存视频和音频
            video_file = f'./biliVideo/{safe_title}.mp4'
            audio_file = f'./biliVideo/{safe_title}.mp3'
            output_file = f'./biliVideo/{safe_title}_output.mp4'

            # 保存视频文件
            with open(video_file, 'wb') as fp:
                fp.write(video_content)

            # 保存音频文件
            with open(audio_file, 'wb') as fp:
                fp.write(audio_content)

            print(f"音频文件和视频文件已保存, 标题: {safe_title}")

            # 合并视频和音频
            merge_audio_video(video_file, audio_file, output_file)

        except KeyError as e:
            print(f"解析播放信息时遇到错误: {e}")
        except requests.exceptions.RequestException as e:
            print(f"下载音频或视频时遇到错误: {e}")
    else:
        print("未找到播放信息，无法下载视频和音频。")

# 主函数，处理多个URL
def process_urls_from_file(file_path, headers):
    # 打开文件并读取URL
    with open(file_path, 'r', encoding='utf-8') as file:
        urls = file.readlines()

    # 去掉每个URL的换行符
    urls = [url.strip() for url in urls]

    # 依次处理每个URL
    for url in urls:
        print(f"正在处理URL: {url}")
        process_bilibili_url(url, headers)
        print(f"已完成URL: {url}\n")

# 设置cookie和headers
cookie = "buvid3=B3E1E8CA-B79D-27F4-C11C-6DD3E6788F8E70365infoc; b_nut=1716513770; _uuid=4A5C7391-7CCC-321F-FAA4-A82A5BA2E35A71017infoc; enable_web_push=DISABLE; buvid4=E2C6B444-BAD5-07C2-C8C9-2E234594DDFD71580-024052401-VZoVl3R9qioHczeP6qdp7A%3D%3D; hit-dyn-v2=1; rpdid=|(uY~~JYJ~ul0J'u~uYluR|)R; header_theme_version=CLOSE; DedeUserID=1194392554; DedeUserID__ckMd5=3e16b07f21dd870a; buvid_fp_plain=undefined; bmg_af_switch=1; bmg_src_def_domain=i1.hdslb.com; CURRENT_FNVAL=4048; go-back-dyn=0; CURRENT_QUALITY=80; share_source_origin=WEIXIN; SESSDATA=9c3c5d6a%2C1741241891%2Cc2809%2A92CjAs-Iu5b6hyxmx0QNYyeoAHC2fuqll4LESO1gLF22nxTjINJigKAuK97ss4KUBQKosSVkZTeEl2dU50dnJCcWJvTEpZTjBBaVQ1SjhzNGtfR213UFNSVlhhYmhnbVItbU1uUE9XemR4Y3Z4WU9uV2t5M0hnZGcxeXd2cGVWV0ZzWGF4TEZYYTlRIIEC; bili_jct=586d3f2e5fa1a40a919e0071983a107e; sid=7j3014lc; fingerprint=8be0ba0ab3bcc882671a99adf0966d40; buvid_fp=8be0ba0ab3bcc882671a99adf0966d40; bp_t_offset_1194392554=975081911200251904; bsource=search_google; home_feed_column=4; browser_resolution=418-757; b_lsid=10AC1D2C6_191D9EE63D5"
headers = {
    'User-Agent': "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/117.0.0.0 Safari/537.36",
    'Referer': 'https://www.bilibili.com/',
    'Cookie': cookie
}

# 读取url.txt文件并处理
process_urls_from_file('url.txt', headers)

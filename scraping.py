import re
import json
import os
import requests
from time import sleep
from lxml import etree
import pprint
import subprocess

# Function to clean the file name by removing illegal characters
def clean_filename(filename):
    # Retain only letters, numbers, underscores, and periods
    return re.sub(r'[^\w\-_\.]', '_', filename)

# Function to merge audio and video
def merge_audio_video(video_file, audio_file, output_file):
    command = [
        'ffmpeg', '-i', video_file, '-i', audio_file, '-c:v', 'copy', '-c:a', 'aac', '-strict', 'experimental', output_file
    ]
    print(f"Merge command: {' '.join(command)}")
    try:
        result = subprocess.run(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        print("stdout:", result.stdout.decode())
        print("stderr:", result.stderr.decode())
        if result.returncode == 0:
            print(f"Audio and video successfully merged into {output_file}")
        else:
            print("Error occurred during merging")
    except subprocess.CalledProcessError as e:
        print(f"Error occurred during merging: {e}")

# Function to crawl and process a single URL
def process_bilibili_url(url, headers):
    response = requests.get(url, headers=headers)
    sleep(2)
    page_text = response.text

    tree = etree.HTML(page_text)

    # Extract the title
    titles = tree.xpath('//title/text()')
    if titles:
        title = titles[0].split('_')[0].strip()  # Only take the main title part
        print(f"Retrieved title: {title}")
    else:
        print("Unable to find title")
        title = "Unknown Title"

    # Clean the title to generate a valid file name
    safe_title = clean_filename(title)

    # Extract play information
    play_info_scripts = tree.xpath('/html/head/script[contains(text(), "window.__playinfo__")]/text()')
    if play_info_scripts:
        play_info = play_info_scripts[0][20:]  # Remove prefix
        play_info_json = json.loads(play_info)
        pprint.pprint(play_info_json)
    else:
        print("Unable to find play information script")
        play_info_json = None

    # Download video and audio
    if play_info_json:
        try:
            video_url = play_info_json['data']['dash']['video'][0]['baseUrl']
            audio_url = play_info_json['data']['dash']['audio'][0]['baseUrl']

            # Download video and audio
            video_content = requests.get(url=video_url, headers=headers).content
            audio_content = requests.get(url=audio_url, headers=headers).content

            # Create directory for saving
            if not os.path.exists('./biliVideo'):
                os.mkdir('./biliVideo')

            # Save video and audio using safe file names
            video_file = f'./biliVideo/{safe_title}.mp4'
            audio_file = f'./biliVideo/{safe_title}.mp3'
            output_file = f'./biliVideo/{safe_title}_output.mp4'

            # Save video file
            with open(video_file, 'wb') as fp:
                fp.write(video_content)

            # Save audio file
            with open(audio_file, 'wb') as fp:
                fp.write(audio_content)

            print(f"Audio and video files saved, title: {safe_title}")

            # Merge video and audio
            merge_audio_video(video_file, audio_file, output_file)

        except KeyError as e:
            print(f"Error encountered while parsing play information: {e}")
        except requests.exceptions.RequestException as e:
            print(f"Error encountered while downloading audio or video: {e}")
    else:
        print("No play information found, unable to download video and audio.")

# Main function to process multiple URLs
def process_urls_from_file(file_path, headers):
    # Open file and read URLs
    with open(file_path, 'r', encoding='utf-8') as file:
        urls = file.readlines()

    # Strip newline characters from each URL
    urls = [url.strip() for url in urls]

    # Process each URL one by one
    for url in urls:
        print(f"Processing URL: {url}")
        process_bilibili_url(url, headers)
        print(f"Finished processing URL: {url}\n")

# Set cookies and headers
# Change to your own cookie
cookie = "buvid3=B3E1E8CA-B79D-27F4-C11C-6DD3E6788F8E70365infoc; b_nut=1716513770; _uuid=4A5C7391-7CCC-321F-FAA4-A82A5BA2E35A71017infoc; enable_web_push=DISABLE; buvid4=E2C6B444-BAD5-07C2-C8C9-2E234594DDFD71580-024052401-VZoVl3R9qioHczeP6qdp7A%3D%3D; hit-dyn-v2=1; rpdid=|(uY~~JYJ~ul0J'u~uYluR|)R; header_theme_version=CLOSE; DedeUserID=1194392554; DedeUserID__ckMd5=3e16b07f21dd870a; buvid_fp_plain=undefined; bmg_af_switch=1; bmg_src_def_domain=i1.hdslb.com; CURRENT_FNVAL=4048; go-back-dyn=0; CURRENT_QUALITY=80; share_source_origin=WEIXIN; SESSDATA=9c3c5d6a%2C1741241891%2Cc2809%2A92CjAs-Iu5b6hyxmx0QNYyeoAHC2fuqll4LESO1gLF22nxTjINJigKAuK97ss4KUBQKosSVkZTeEl2dU50dnJCcWJvTEpZTjBBaVQ1SjhzNGtfR213UFNSVlhhYmhnbVItbU1uUE9XemR4Y3Z4WU9uV2t5M0hnZGcxeXd2cGVWV0ZzWGF4TEZYYTlRIIEC; bili_jct=586d3f2e5fa1a40a919e0071983a107e; sid=7j3014lc; fingerprint=8be0ba0ab3bcc882671a99adf0966d40; buvid_fp=8be0ba0ab3bcc882671a99adf0966d40; bp_t_offset_1194392554=975081911200251904; bsource=search_google; home_feed_column=4; browser_resolution=418-757; b_lsid=10AC1D2C6_191D9EE63D5"
headers = {
    'User-Agent': "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/117.0.0.0 Safari/537.36",
    'Referer': 'https://www.bilibili.com/',
    'Cookie': cookie
}

# Read url.txt file and process it
process_urls_from_file('url.txt', headers)

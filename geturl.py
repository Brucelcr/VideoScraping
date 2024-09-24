import requests
from lxml import html

def extract_video_urls_from_bilibili_page(url):
    # 添加请求头，模拟浏览器访问
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
    }
    
    # 发起HTTP请求获取页面内容
    response = requests.get(url, headers=headers)
    
    # 检查请求是否成功
    if response.status_code != 200:
        print(f"无法获取页面，状态码: {response.status_code}")
        return []
    
    # 使用lxml解析HTML内容
    tree = html.fromstring(response.content)
    
    # 提取所有<a>标签中的href属性（即URL）
    urls = tree.xpath('//a/@href')
    
    # 使用set去重
    video_urls = set()
    for url in urls:
        if '/video/' in url:
            if url.startswith('http'):
                video_urls.add(url)
            elif url.startswith('//'):
                video_urls.add('https:' + url)
            else:
                video_urls.add('https://www.bilibili.com' + url)
    
    return list(video_urls)

def save_urls_to_file(urls, filename):
    with open(filename, 'w', encoding='utf-8') as file:
        for url in urls:
            file.write(url + '\n')
    print(f"已将 {len(urls)} 个视频URL保存到 {filename} 文件中。")

# 示例：B站页面URL
bilibili_page_url = "https://search.bilibili.com/all?keyword=%E8%8B%B1%E6%96%87%E8%A7%86%E9%A2%91&from_source=webtop_search&spm_id_from=333.1007&search_source=3"

# 提取页面中的所有视频URL  
video_urls = extract_video_urls_from_bilibili_page(bilibili_page_url)

# 将视频URL保存到url.txt文件中
save_urls_to_file(video_urls, 'url.txt')

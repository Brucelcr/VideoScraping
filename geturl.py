import requests
from lxml import html

# Function to extract video URLs from a Bilibili page
def extract_video_urls_from_bilibili_page(url):
    # Add request headers to simulate a browser visit
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
    }
    
    # Make an HTTP request to get the page content
    response = requests.get(url, headers=headers)
    
    # Check if the request was successful
    if response.status_code != 200:
        print(f"Failed to retrieve page, status code: {response.status_code}")
        return []
    
    # Use lxml to parse the HTML content
    tree = html.fromstring(response.content)
    
    # Extract all href attributes from <a> tags (i.e., URLs)
    urls = tree.xpath('//a/@href')
    
    # Use a set to remove duplicates
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

# Function to save URLs to a file
def save_urls_to_file(urls, filename):
    with open(filename, 'w', encoding='utf-8') as file:
        for url in urls:
            file.write(url + '\n')
    print(f"Saved {len(urls)} video URLs to the {filename} file.")

# Example: Bilibili page URL
bilibili_page_url = "https://search.bilibili.com/all?keyword=%E8%8B%B1%E6%96%87%E8%A7%86%E9%A2%91&from_source=webtop_search&spm_id_from=333.1007&search_source=3"

# Extract all video URLs from the page
video_urls = extract_video_urls_from_bilibili_page(bilibili_page_url)

# Save the video URLs to the url.txt file
save_urls_to_file(video_urls, 'url.txt')

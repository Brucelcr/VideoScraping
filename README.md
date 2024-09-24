# VideoScraping

Automated and batch scraping of videos and information from Bilibili (China's equivalent of YouTube) using keywords. You can also scrape content directly from a specific user's homepage.

# Why did I write this program?

I wrote this program because I needed a large number of videos for AI translation testing. I found that there weren’t any existing scripts online that could automatically and batch-scrape Bilibili videos. So, I decided to write one myself and share it, so others can use it in the future. Bilibili offers individual video downloads, but it doesn’t support batch downloads, which is also the limitation of most scripts available online.

# How does this script work, and what is the principle behind it?

In simple terms, this script works by first collecting the URLs of videos from Bilibili in bulk (using `geturl.py`) and saving them to a `url.txt` file. Then, `scraping.py` processes this text file by recursion going through each video URL one by one. After obtaining the URL, the script scrapes the webpage to download both the video and audio, along with other details like the title. It then uses **ffmpeg** to merge the video and audio files into a complete video with sound, saving the final video in the `biliVideo` folder.

# How to Use This Script

To use this script, you'll need to configure a Python environment on your local machine and install **ffmpeg**. Follow these steps:

## Steps to Use the Script:

### 1. Install Python
- Make sure you have Python installed (preferably Python 3.x). You can download Python from [python.org](https://www.python.org/downloads/).
- After installation, confirm it's installed correctly by running the following command in your terminal or command prompt:
  ```bash
  python --version
  ```

### 2. Set up a Virtual Environment (Optional but recommended)
- It’s a good practice to create a virtual environment for your Python projects:
  ```bash
  python -m venv myenv
  source myenv/bin/activate  # On Windows, use `myenv\Scripts\activate`
  ```

### 3. Install Required Python Libraries
- Navigate to the directory where your `geturl.py` and `crawl.py` scripts are located.
- If the script uses third-party libraries, install them using `pip`. Based on the likely requirements for web scraping, install the necessary libraries like `requests` and `lxml`:
  ```bash
  pip install requests lxml
  ```

### 4. Install ffmpeg
- **Windows**:
  - Download the FFmpeg executable from [FFmpeg's official website](https://ffmpeg.org/download.html).
  - Unzip it and add the `bin` folder to your system’s PATH.
  - To confirm it's installed, run:
    ```bash
    ffmpeg -version
    ```
  
- **macOS/Linux**:
  - On macOS, you can use Homebrew:
    ```bash
    brew install ffmpeg
    ```
  - On Linux (Debian-based systems):
    ```bash
    sudo apt-get install ffmpeg
    ```

### 5. Run the Script
- First, execute `geturl.py` to collect the video URLs in bulk. This will save the URLs in a `url.txt` file:
  ```bash
  python geturl.py
  ```

- Once you have the URLs, run `crawl.py` to scrape the individual videos and merge their audio and video using ffmpeg:
  ```bash
  python crawl.py
  ```

### 6. Check the Output
- The final merged videos with sound will be saved in the `biliVideo` folder on your computer.

```


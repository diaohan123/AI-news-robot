from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from utils.utils import is_target_date, get_response_from_website, load_config
import requests
import json
import platform
import random
import os
from selenium.webdriver.chrome.service import Service as ChromeService
from webdriver_manager.chrome import ChromeDriverManager


class AI_scrapper:
    def __init__(self, url=None):
        self.url = url
        chromeOptions = Options()
        chromeOptions.add_argument("--headless")
        chromeOptions.add_argument("--no-sandbox")
        chromeOptions.add_argument("--disable-dev-shm-usage")
        
        
        # 随机选择一个 User-Agent
        user_agents = [
            "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36",
            "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36",
            "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36",
            "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:123.0) Gecko/20100101 Firefox/123.0",
        ]
        chromeOptions.add_argument(f"user-agent={random.choice(user_agents)}")

        # 添加更多的请求头参数
        chromeOptions.add_argument("--accept-language=zh-CN,zh;q=0.9,en;q=0.8")
        chromeOptions.add_argument(
            "--accept=text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7"
        )
        chromeOptions.add_argument(
            '--sec-ch-ua="Chromium";v="122", "Google Chrome";v="122", "Not(A:Brand";v="24"'
        )
        chromeOptions.add_argument("--sec-ch-ua-mobile=?0")
        chromeOptions.add_argument('--sec-ch-ua-platform="Windows"')

        os_name = platform.system()
        current_dir = os.path.dirname(os.path.abspath(__file__))
        if os_name == "Darwin":
            service = Service(
                os.path.join(current_dir, "chromedriver-mac-arm64/chromedriver")
            )
        elif os_name == "Linux":
            service = Service(
                os.path.join(current_dir, "chromedriver-linux64/chromedriver")
            )
        else:
            service = ChromeService(ChromeDriverManager().install())
        self.options = chromeOptions
        self.service = service
        self.config = load_config()
        
    def scrap_news_info(self, url):
        payload = json.dumps({"url": url})
        headers = {
            "X-API-KEY": self.config['serper']['api_key'],
            "Content-Type": "application/json",
        }
        response = requests.request(
            "POST", self.config['serper']['base_url'], headers=headers, data=payload
        )
        response = response.json()
        content = response["text"]
        metadata = response["metadata"]
        title = metadata.get("og:title")
        image = metadata.get("og:image")
        # date = metadata.get("article:published_time")
        return [title, content, url, image]

    def find_news_by_date(self, target_date):
        urls = self.find_urls()
        news_list = []
        for url in urls:
            date = self.get_website_publication_date(url)
            if is_target_date(date, target_date):
                news_list.append(url)
        return news_list

    def _is_url_accessible(self, url):
        try:
            response = get_response_from_website(url)
            return response.status_code == 200
        except Exception as e:
            print(f"访问出错: {str(e)} - URL: {url}")
            return False

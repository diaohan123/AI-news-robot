from selenium import webdriver
from selenium.webdriver.common.by import By
from bs4 import BeautifulSoup
from utils.utils import parse_and_format_date
from .scrapper import AI_scrapper
import requests


class AI_scrapper_xiaohu(AI_scrapper):
    def __init__(self):
        super().__init__(url="https://xiaohu.ai/c/ainews")

    def find_urls(self, num=5):
        driver = webdriver.Chrome(service=self.service, options=self.options)
        try:
            # 打开一个网页
            driver.get(self.url)
            # 等待页面加载完成，可以根据需要设定等待条件
            driver.implicitly_wait(5)
            # 抓取动态加载的内容
            link_elements = driver.find_elements(By.TAG_NAME, "a")
            urls = []

            for link in link_elements:
                href = link.get_attribute("href")
                end = href.split("/")[-1]
                if end.isdigit() and href not in urls:
                    urls.append(href)
        except Exception as e:
            print("抓取链接错误" + self.url, e)
            return []
        finally:
            driver.quit()
        return urls[:num]

    def get_website_publication_date(self, url: str):
        try:
            response = requests.get(url)
            response.raise_for_status()  # 检查请求是否成功
            soup = BeautifulSoup(response.text, "html.parser")
            # 从<meta>标签获取发布日期
            meta_date = soup.find("meta", attrs={"property": "article:published_time"})
            if meta_date and meta_date.has_attr("content"):
                parsed_date = parse_and_format_date(meta_date["content"])
                if parsed_date:
                    return parsed_date
            # 没有找到发布日期
            return "No publication date found"
        except requests.exceptions.RequestException as e:
            return f"An error occurred: {e}"

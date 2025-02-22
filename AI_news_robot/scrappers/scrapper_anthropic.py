from selenium import webdriver
from selenium.webdriver.common.by import By
from utils.utils import parse_and_format_date
from .scrapper import AI_scrapper


class AI_scrapper_anthropic(AI_scrapper):
    def __init__(self):
        super().__init__(url="https://www.anthropic.com/news")

    def find_urls(self, num=5):
        driver = webdriver.Chrome(service=self.service, options=self.options)
        urls = []
        # 打开一个网页
        try:
            driver.get(self.url)
            driver.implicitly_wait(2)
            all_links = driver.find_elements(By.TAG_NAME, "a")
            for link in all_links:
                href = link.get_attribute("href")
                if href and href not in urls and href not in self.url:
                    if "/news/" in href or "research/" in href:
                        urls.append(href)
        except Exception as e:
            print("抓取链接错误" + self.url, e)
            return []
        return urls[:num]

    def get_website_publication_date(self, url: str):
        """
        使用selenium从网页中提取发布日期
        返回格式：YYYY-MM-DD
        """
        driver = webdriver.Chrome(service=self.service, options=self.options)
        try:
            driver.get(url)
            driver.implicitly_wait(2)
            selector = '//*[contains(@class, "time")]'
            elements = driver.find_elements(By.XPATH, selector)
            if elements:
                date_str = elements[0].text
                if date_str:
                    return parse_and_format_date(date_str.split("\n")[0])
            print("no date found in " + url)
        except Exception as e:
            print("抓取日期错误" + url, e)
        finally:
            driver.quit()

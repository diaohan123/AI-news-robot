from selenium import webdriver
from selenium.webdriver.common.by import By
from utils.utils import parse_and_format_date, is_target_date
from .scrapper import AI_scrapper
import json


class AI_scrapper_google_technology(AI_scrapper):
    def __init__(self):
        url = "https://blog.google/technology/"
        super().__init__(url=url)

    def find_news_by_date(self, target_date):
        driver = webdriver.Chrome(service=self.service, options=self.options)
        try:
            driver.get(self.url)
            driver.implicitly_wait(2)
            urls = []
            articles = driver.find_elements(
                By.CSS_SELECTOR, "[data-ga4-analytics-lead-click]"
            )
            for article in articles:
                try:
                    data_attr = article.get_dom_attribute(
                        "data-ga4-analytics-lead-click"
                    )
                    data_json = json.loads(data_attr)
                    date_str = data_json.get("publish_date", "").split("|")[0].strip()
                    if date_str and is_target_date(date_str, target_date):
                        # 获取 page_name
                        page_name = data_json.get("page_name", "").split("|")[0].strip()
                        # 查找包含 page_name 的链接
                        links = driver.find_elements(
                            By.XPATH, f".//a[contains(@href, '{page_name}')]"
                        )
                        for link in links:
                            href = link.get_attribute("href")
                            if href and href not in urls:
                                urls.append(href)
                except Exception as e:
                    continue
        except Exception as e:
            print(f"抓取链接错误 {self.url}: {str(e)}")
            return []
        finally:
            driver.quit()
        return urls

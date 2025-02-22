from selenium import webdriver
from selenium.webdriver.common.by import By
from utils.utils import parse_and_format_date, is_target_date
from .scrapper import AI_scrapper


class AI_scrapper_venturebeat(AI_scrapper):
    def __init__(self):
        super().__init__(url="https://venturebeat.com/tag/ai-ml-deep-learning/")

    def find_news_by_date(self, target_date):
        driver = webdriver.Chrome(service=self.service, options=self.options)
        try:
            driver.get(self.url)
            driver.implicitly_wait(2)
            urls = []
            # 使用  class 选择器来定位文章列表项
            articles = driver.find_elements(By.CLASS_NAME, "ArticleListing__time")
            for article in articles:
                date_str = article.get_dom_attribute("datetime")
                if date_str:
                    article_date = parse_and_format_date(date_str)
                    if is_target_date(article_date, target_date):
                        # 从时间元素向上查找到标题链接
                        parent_article = article.find_element(
                            By.XPATH,
                            "../..//a[contains(@class, 'ArticleListing__title-link')]",
                        )
                        href = parent_article.get_dom_attribute("href")
                        if href and href not in urls:
                            urls.append(href)
        except Exception as e:
            print("抓取链接错误" + self.url, e)
            return []
        finally:
            driver.quit()
        return urls

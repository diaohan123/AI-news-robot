from selenium import webdriver
from selenium.webdriver.common.by import By
from utils.utils import parse_and_format_date, is_target_date
from .scrapper import AI_scrapper


class AI_scrapper_deepmind(AI_scrapper):
    def __init__(self):
        url = "https://deepmind.google/discover/blog/"
        super().__init__(url=url)

    def find_news_by_date(self, target_date):
        driver = webdriver.Chrome(service=self.service, options=self.options)
        try:
            driver.get(self.url)
            driver.implicitly_wait(2)
            urls = []
            # 使用正确的类名选择器定位文章列表项
            articles = driver.find_elements(
                By.CSS_SELECTOR, "span.glue-label.card__publish-date time"
            )
            for article in articles:
                date_str = article.get_dom_attribute("datetime")
                if date_str:
                    article_date = parse_and_format_date(date_str)
                    if is_target_date(article_date, target_date):
                        # 从时间元素向上查找到文章链接
                        parent_article = article.find_element(
                            By.XPATH, "ancestor::a[contains(@class, 'glue-card')]"
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

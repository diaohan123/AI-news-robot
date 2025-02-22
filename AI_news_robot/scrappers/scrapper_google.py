from selenium import webdriver
from selenium.webdriver.common.by import By
from utils.utils import parse_and_format_date, is_target_date
from .scrapper import AI_scrapper


class AI_scrapper_google(AI_scrapper):
    def __init__(self):
        url = "https://research.google/blog/"
        super().__init__(url=url)

    def find_news_by_date(self, target_date):
        driver = webdriver.Chrome(service=self.service, options=self.options)
        try:
            driver.get(self.url)
            driver.implicitly_wait(2)
            urls = []
            # 找到所有文章卡片
            articles = driver.find_elements(By.CSS_SELECTOR, "a.glue-card")
            for article in articles:
                # 在每个卡片中找到日期标签
                date_element = article.find_element(
                    By.CSS_SELECTOR, "p.glue-label.glue-spacer-1-bottom"
                )
                date_text = date_element.text
                article_date = parse_and_format_date(date_text)
                if is_target_date(article_date, target_date):
                    href = article.get_dom_attribute("href")
                    if href:
                        url = "https://research.google" + href
                        if url not in urls:
                            urls.append(url)
        except Exception as e:
            print("抓取链接错误" + self.url, e)
            return []
        finally:
            driver.quit()
        return urls


if __name__ == "__main__":
    scrapper = AI_scrapper_google()
    urls = scrapper.find_news_by_date("2025-02-10")
    print(urls)

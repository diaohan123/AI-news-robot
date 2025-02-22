from selenium import webdriver
from selenium.webdriver.common.by import By
from .scrapper import AI_scrapper
from datetime import datetime


class AI_scrapper_openai(AI_scrapper):
    def __init__(self):
        url = "https://openai.com/news"
        super().__init__(url=url)

    def find_news_by_date(self, target_date):
        driver = webdriver.Chrome(service=self.service, options=self.options)
        try:
            driver.get(self.url)
            driver.implicitly_wait(2)
            urls = []
            date_str = datetime.strptime(target_date, "%Y-%m-%d").strftime("%b %d, %Y")

            xpath_expression = f"//span[contains(text(), '{date_str}')]"
            time_elements = driver.find_elements(By.XPATH, xpath_expression)

            for time_element in time_elements:
                try:
                    # 向上查找最近的a标签
                    parent_link = time_element.find_element(By.XPATH, "ancestor::a")
                    href = parent_link.get_attribute("href")
                    date = time_element.text
                    print(f"链接: {href}, 日期: {date}")
                    if href not in urls and href not in self.url:
                        urls.append(href)
                except:
                    continue

        except Exception as e:
            print("抓取链接错误" + self.url, e)
            return []
        finally:
            driver.quit()
        return urls

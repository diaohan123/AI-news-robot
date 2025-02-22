from datetime import datetime
from .scrapper import AI_scrapper


class AI_scrapper_jiqizhixin(AI_scrapper):
    def __init__(self):
        super().__init__(url="https://www.jiqizhixin.com/")

    def find_news_by_date(self, date):
        date = datetime.strptime(date, "%Y-%m-%d").date()
        urls = []
        base_url = f"https://www.jiqizhixin.com/articles/{date}"
        if self._is_url_accessible(base_url + "/"):
            urls.append(base_url + "/")
        i = 2
        for i in range(2, 20):
            url = f"{base_url}-{i}/"
            if self._is_url_accessible(url):
                urls.append(url)
            i += 1
        return urls

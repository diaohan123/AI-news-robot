from datetime import datetime
import requests
import json
from news_editor import news_editor
from utils.utils import load_config

class news_robot:
    def __init__(
        self,
        webhook,
    ):
        self.webhook = webhook

    def set_date(self, date):
        self.date = date

    def send_message(self, url_list, webhook=None):
        if webhook is None:
            webhook = self.webhook
        editor = news_editor(date=self.date)
        editor.clean_news()
        for url in url_list:
            editor.add_news(url)
        card = editor.create_full_template()
        message = {"msg_type": "interactive", "card": card}
        response = requests.post(
            url=webhook,
            data=json.dumps(message),
            headers={"Content-Type": "application/json"},
        )
        print(response.text)
        # 检查响应状态码
        if response.status_code == 200:
            print("消息发送成功！")
            success = True
        else:
            print(
                "发送失败，状态码：", response.status_code, "响应内容：", response.text
            )
            success = False
        editor.clean_news()
        return success

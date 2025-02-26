from scrappers import *
from news_robot import news_robot
from datetime import datetime, timedelta
from utils.utils import load_config
import schedule
import time


def job(webhook: str, date: str = None):
    robot = news_robot(webhook=webhook)
    scrapers = [
        AI_scrapper_openai(),
        AI_scrapper_deepmind(),
        AI_scrapper_google_technology(),
        AI_scrapper_google(),
        AI_scrapper_anthropic(),
        AI_scrapper_xiaohu(),
        AI_scrapper_jiqizhixin(),
        AI_scrapper_venturebeat(),
    ]
    if date is None:
        date = (datetime.now() - timedelta(days=1)).strftime("%Y-%m-%d")
    robot.set_date(date)
    current_time = datetime.now()
    print(f"当前时间: {current_time.strftime('%Y-%m-%d %H:%M:%S')}")
    total_urls = []
    for scrapper in scrapers:
        try:
            urls = scrapper.find_news_by_date(date)
            print(f"{scrapper.__class__.__name__} 获取到 {len(urls)} 条新闻\n{urls}")
            total_urls.extend(urls)
        except Exception as e:
            print(f"爬取 {scrapper.__class__.__name__} 时出错: {str(e)}")
            continue

    try:
        robot.send_message(total_urls)
        print(f"成功推送 {len(total_urls)} 条新闻")
    except Exception as e:
        print(f"发送新闻时出错: {str(e)}")
        print(f"错误类型: {type(e)}")


if __name__ == "__main__":
    config = load_config()
    # 群聊链接
    ai_group_url = config['feishu_webhook']['group']
    # 测试链接
    test_url = config['feishu_webhook']['test']

    # 首次运行
    job(webhook=test_url)

    # 设置定时任务
    schedule.every().day.at(config['schedule']['time']).do(job, webhook=ai_group_url)

    # 主循环
    while True:
        try:
            print(f'current time: {datetime.now().strftime("%Y-%m-%d %H:%M:%S")}')
            schedule.run_pending()
            time.sleep(59)  # 改为每分钟检查一次
        except Exception as e:
            print(f"主循环出错: {str(e)}")
            time.sleep(59)  # 出错后等待一分钟继续

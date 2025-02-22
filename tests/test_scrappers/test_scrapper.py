import sys
import os

# 获取当前文件的绝对路径
current_dir = os.path.dirname(os.path.abspath(__file__))
# 获取项目根目录的路径（向上两级）
project_root = os.path.dirname(os.path.dirname(current_dir))
# 添加项目根目录到 Python 路径
sys.path.append(project_root)

from AI_news_robot.scrappers import *

if __name__ == "__main__":
    scrapper = AI_scrapper_google()
    print(scrapper.find_news_by_date("2025-02-10"))

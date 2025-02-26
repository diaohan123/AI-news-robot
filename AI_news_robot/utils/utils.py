from datetime import datetime
from dateutil import parser
import requests
import json
import yaml
import os

def load_config():
    """Load config from yaml file and return Config instance"""
    config_file_path = os.getenv(
        "FAWKES_CONFIG_FILE_PATH",
        os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(__file__))), "config.yaml"),
    )

    with open(config_file_path, "r") as f:
        cfg = yaml.safe_load(f)

    return cfg


def is_date_today(date_str: str) -> bool:
    try:
        # 解析给定的日期字符串
        given_date = datetime.strptime(date_str, "%Y-%m-%d").date()
        # 获取当前日期
        today_date = datetime.today().date()
        # 判断给定日期是否为今天
        return given_date == today_date
    except ValueError:
        # 如果日期字符串格式不正确，返回False
        return False

def is_target_date(date_string, target_date):
    """
    判断给定的日期字符串是否是目标日期。
    :param date_string: 日期字符串，格式为 'YYYY-MM-DD'
    :param target_date: 目标日期字符串，格式为 'YYYY-MM-DD'
    :return: 如果日期是目标日期，返回 True，否则返回 False
    """
    if not date_string or not target_date:  # 增加空值检查
        return False        
    date_format = "%Y-%m-%d"
    try:
        date = datetime.strptime(date_string, date_format).date()
        target = datetime.strptime(target_date, date_format).date()
    except (ValueError, TypeError):
        print(f"日期格式错误: {date_string} 或 {target_date}")
        return False
        
    return date == target

def parse_and_format_date(date_str):
    try:
        if '年' in date_str and '月' in date_str and '日' in date_str:
            date_str = date_str.replace('年', '-').replace('月', '-').replace('日', '')
        date = parser.parse(date_str,fuzzy=True)
        return date.strftime("%Y-%m-%d")
    except ValueError as e:
        return None

def get_response_from_serper(url):
    config = load_config()
    payload = json.dumps({"url": url})
    headers = {
        "X-API-KEY": config['serper']['api_key'],
        "Content-Type": "application/json",
    }
    response = requests.request("POST", config['serper']['base_url'], headers=headers, data=payload)
    return response.json()

def get_response_from_website(url):
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36',
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
        'Accept-Language': 'en-US,en;q=0.5',
        'Accept-Encoding': 'gzip, deflate, br',
        'Connection': 'keep-alive',
        'Upgrade-Insecure-Requests': '1',
        'Cache-Control': 'max-age=0'
    }
    response = requests.head(url, headers=headers, allow_redirects=True)
    return response
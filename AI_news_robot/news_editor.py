import requests
from openai import OpenAI
from requests_toolbelt import MultipartEncoder
from pydantic import BaseModel
from utils.utils import get_response_from_serper, load_config
import json


class summary_format(BaseModel):
    title: str
    summary: str
    score: int


def AI_summary(content):
    config = load_config()
    client = OpenAI(
        base_url=config['openai']['base_url'],
        api_key=config['openai']['api_key'],
    )
    completion = client.beta.chat.completions.parse(
        model="gpt-4o-2024-08-06",
        messages=[
            {
                "role": "system",
                "content": (
                    """
                    你是一名新闻摘要师，擅长生成简洁且信息丰富的AI领域新闻摘要。根据提供的输入新闻内容生成新闻摘要。此外，创建一个标题，并评估新闻在AI行业中特别是生成式AI子领域的相关性，给出1到5的评分。请以结构化格式输出。无论输入是哪种语言，输出都必须是中文。

                    # 步骤

                    1. 阅读输入新闻内容。
                    2. 提取关键信息点，如事件、时间、影响和未来展望。
                    3. 生成简明摘要，确保不超过100字。
                    4. 确保摘要连贯且可读，避免过于专业的术语。
                    5. 确定新闻传播者和实际发布者，如平台：小虎AI学院、机器之心。
                    6. 为新闻摘要创建一个合适的标题。
                    7. 评估新闻在AI行业中特别是生成式AI子领域的相关性，并赋予1到5的评分。

                    # 输出格式要求

                    输出必须是一个JSON格式的字符串，包含以下字段:
                    {
                        "title": "标题",
                        "summary": "摘要内容",
                        "score": 评分数字
                    }

                    # 示例

                    输入: "2023年10月，OpenAI发布了最新的GPT-4模型，该模型在自然语言处理任务上表现出色。发布会在旧金山举行，吸引了众多科技界人士参与。OpenAI表示，GPT-4将进一步推动AI技术的发展，并计划在未来几个月内推出更多相关应用。"

                    输出: {"title": "OpenAI发布GPT-4，引领AI技术新潮流", "summary": "2023年10月，OpenAI在旧金山发布了最新的GPT-4模型，该模型在自然语言处理任务上表现出色。此次发布会吸引了众多科技界人士参与。OpenAI表示，GPT-4将推动AI技术的发展，并计划在未来几个月内推出更多应用。", "score": 5}

                    # 评分标准

                    1分: 与AI行业关系很小的新闻(如奖学金评选)
                    2分: 与AI生成式AI无关的新闻(如机器人研究、深度学习理论、AI伦理等)
                    3分: 与生成式AI有一定关联的新闻(如行业访谈、经验分享)
                    4分: 与生成式AI密切相关的新闻(如模型更新、测试、应用方法等等)
                    5分: 官方网站发出的新闻（如openai, anthropic, deepmind 等公司的新模型发布)
                    """
                ),
            },
            {"role": "user", "content": content},
        ],
        response_format=summary_format,
    )
    response = completion.choices[0].message.parsed
    return response.title, response.summary, response.score


def uploadImage(image_url):
    url = "https://open.feishu.cn/open-apis/im/v1/images"
    response = requests.get(image_url)
    if response.status_code == 200:
        image_data = response.content
    form = {"image_type": "message", "image": image_data}  # 需要替换具体的path
    multi_form = MultipartEncoder(form)
    headers = {
        "Authorization": "Bearer t-g104c3i5VPNMHI2ZFXDUFPCEHPY7F25WXEXSQKCF",  ## 获取tenant_access_token, 需要替换为实际的token
    }
    headers["Content-Type"] = multi_form.content_type
    response = requests.request("POST", url, headers=headers, data=multi_form)
    print(response.headers["X-Tt-Logid"])  # for debug or oncall
    print(response.content)  # Print Response
    return response.content


class news_editor:
    def __init__(self, date, tags=[], news_list=[]):
        self.date = date
        self.tags = tags
        self.news_list = news_list
        pass

    def set_date(self, date):
        self.date = date

    def clean_news(self):
        self.news_list = []

    def add_news(self, url):
        try:
            response = get_response_from_serper(url)
            content = response["text"]
        except Exception as e:
            print(f"serper 抓取{url}内容失败: {str(e)}")
            return
        try:
            title, summary, score = AI_summary(content)
            print(title, score)
        except Exception as e:
            print(f"AI 摘要失败: {str(e)}, 内容: {content}")
            return
        if score <= 3:
            return
        metadata = response["metadata"]
        # title = metadata.get("og:title")
        site_name = metadata.get("og:site_name")
        if site_name is None:
            if "anthropic" in url:
                site_name = "Anthropic"
            elif "openai" in url:
                site_name = "OpenAI"
            elif "google" in url:
                site_name = "Google"
        self.news_list.append([title, summary, url, site_name])

    def create_full_template(self):
        template = {
            "config": {"update_multi": True},
            "i18n_elements": {
                "zh_cn": [],
            },
            "i18n_header": {"zh_cn": {}},
        }
        for news in self.news_list:
            title, content, url, site_name = news
            template["i18n_elements"]["zh_cn"].append(
                self.create_news_template(title, content, url, site_name)
            )
        template["i18n_header"]["zh_cn"] = self.create_title_template(
            self.date, self.tags
        )
        return template

    def create_title_template(self, date: str, tags=[]):
        template = {
            "title": {
                "tag": "plain_text",
                "content": f"AI 快讯播报！快来看看「{date}」有哪些AI新闻吧",
            },
            "subtitle": {"tag": "plain_text", "content": ""},
            "text_tag_list": [],
            "template": "indigo",
            "icon": {
                "tag": "custom_icon",
                "img_key": "img_v3_027m_91fb8fc2-e6a3-406c-aa9d-04569e29bccg",
            },
        }
        for tag in tags:
            tag_template = {
                "tag": "text_tag",
                "text": {"tag": "plain_text", "content": tag},
                "color": "orange",
            }
            template["text_tag_list"].append(tag_template)
        return template

    def create_news_template(self, title: str, content: str, url: str, site_name=None):
        template = {
            "tag": "column_set",
            "flex_mode": "none",
            "horizontal_spacing": "8px",
            "horizontal_align": "left",
            "columns": [
                {
                    "tag": "column",
                    "width": "weighted",
                    "vertical_align": "top",
                    "vertical_spacing": "8px",
                    "elements": [
                        {
                            "tag": "markdown",
                            "content": f"**{title}**",
                            "text_align": "left",
                            "text_size": "normal",
                        },
                        {
                            "tag": "markdown",
                            "content": content,
                            "text_align": "left",
                            "text_size": "notation",
                        },
                        {
                            "tag": "column_set",
                            "flex_mode": "none",
                            "horizontal_spacing": "8px",
                            "horizontal_align": "left",
                            "columns": [
                                {
                                    "tag": "column",
                                    "width": "weighted",
                                    "vertical_align": "top",
                                    "elements": [
                                        {
                                            "tag": "button",
                                            "text": {
                                                "tag": "plain_text",
                                                "content": "查看详情",
                                            },
                                            "type": "primary",
                                            "width": "default",
                                            "size": "small",
                                            "icon": {
                                                "tag": "standard_icon",
                                                "token": "laser_outlined",
                                            },
                                            "behaviors": [
                                                {
                                                    "type": "open_url",
                                                    "default_url": url,
                                                    "pc_url": "",
                                                    "ios_url": "",
                                                    "android_url": "",
                                                }
                                            ],
                                        }
                                    ],
                                    "weight": 1,
                                },
                                {
                                    "tag": "column",
                                    "width": "weighted",
                                    "vertical_align": "top",
                                    "elements": [
                                        {
                                            "tag": "markdown",
                                            "content": f"*--{site_name}--* ",
                                            "text_align": "right",
                                            "text_size": "notation",
                                        }
                                    ],
                                    "weight": 1,
                                },
                            ],
                            "margin": "0px 0px 0px 0px",
                        },
                    ],
                    "weight": 1,
                },
                {
                    "tag": "column",
                    "width": "auto",
                    "vertical_align": "top",
                    "vertical_spacing": "8px",
                    "elements": [
                        {
                            "tag": "column_set",
                            "flex_mode": "none",
                            "horizontal_spacing": "default",
                            "background_style": "default",
                            "columns": [
                                {
                                    "tag": "column",
                                    "elements": [
                                        {
                                            "tag": "div",
                                            "text": {
                                                "tag": "plain_text",
                                                "content": "",
                                                "text_size": "normal",
                                                "text_align": "left",
                                                "text_color": "default",
                                            },
                                        }
                                    ],
                                    "width": "weighted",
                                    "weight": 1,
                                }
                            ],
                        }
                    ],
                },
            ],
            "margin": "16px 0px 0px 0px",
        }
        return template

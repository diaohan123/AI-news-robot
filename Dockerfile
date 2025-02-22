FROM python:3.10-slim
# FROM selenium/standalone-chrome:latest
# 设置工作目录
WORKDIR /AI_news_robot

# 将当前目录下的所有文件复制到工作目录
COPY . /AI_news_robot

RUN apt-get update && \
    apt-get install -y \
      chromium=131.* \
      chromium-sandbox=131.* \
      chromium-common=131.* \
    && apt-get clean && \
    rm -rf /var/lib/apt/lists/*

# 安装应用所需的依赖
RUN pip install selenium &&\
    pip install webdriver_manager &&\
    pip install requests &&\
    pip install beautifulsoup4 &&\
    pip install python-dateutil &&\
    pip install schedule &&\
    pip install openai &&\
    pip install requests_toolbelt &&\
    pip install pydantic

# RUN chmod +x AI_news_robot/chromedriver

# 运行
CMD ["python", "AI_news_robot/main.py"]

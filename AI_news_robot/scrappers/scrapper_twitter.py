from AI_news_robot.scrappers.scrapper import *
from news_robot import news_robot
from datetime import datetime, timezone
import tweepy

def summary_twitter(content):
    completion = client.beta.chat.completions.parse(
        model="gpt-4o-2024-08-06",
        messages=[
            {
                "role": "system",
                "content": (
                    """
                    从 Twitter 博主的一天帖子中总结有用的信息，并整理成几个要点。每个要点应包含标题、内容和相关链接。

                    # Steps

                    1. 浏览博主的当天帖文。
                    2. 提取出每条帖文中的关键信息。
                    3. 总结这些信息，突出重要性或有趣之处。
                    4. 提供相应的帖文链接进行引用。

                    # Output Format

                    为每个要点输出如下结构：

                    - **标题**: [帖子标题或主题]
                    - **内容**: [帖文中传达的信息或总结]
                    - **相关链接**: [相应帖文的链接]

                    # Examples

                    - **标题**: 新产品发布
                    **内容**: 博主讨论了品牌的新产品特点和市场期望。
                    **相关链接**: [https://twitter.com/example/status/1234567890]
                    """
                ),
            },
            {"role": "user", "content": content},
        ],
        response_format=summary_format
    )



# 填入你从开发者平台获取的密钥
consumer_key = "ZZsSb1RToJa6gTJb4b4AVFYl5"
consumer_secret = "zg8PfaQna1Oz24pLuiIcF8PEKhkWbmgRh3RDMQBcyQOCY5u1Oo"
access_token = "1864934787385053184-xdjDzEtFVmKannk9kXQSqXUbfxovKL"
access_token_secret = "uASRL7MtsHUMHxXmC7U8VF5MKZqtkzWdrMgC5Y4prlAyq"

# 认证
auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_token, access_token_secret)

# 创建API对象
api = tweepy.API(auth)

# 创建API对象
client = tweepy.Client(
    bearer_token="AAAAAAAAAAAAAAAAAAAAAHfMxgEAAAAAS1TAZ2fBdO9aMPJDSfCQ%2FXeOeV4%3DocqrDzszPRlQQEJoSGqTudsp9FhoOfn9RJlrSn2pdia7rCJmpH",
    consumer_key=consumer_key, 
    consumer_secret=consumer_secret,
    access_token=access_token, 
    access_token_secret=access_token_secret
)
try:
    # 测试认证是否成功
    api.verify_credentials()
    print("Authentication OK")
except:
    print("Error during authentication")
    
try:
    # 首先获取用户 ID
    user = client.get_user(username="dotey")
    if user.data:
        user_id = user.data.id
        
        # 设置开始时间和结束时间（UTC时间）
        start_time = datetime(2024, 12, 24, tzinfo=timezone.utc)  
        end_time = datetime(2024, 12, 24, tzinfo=timezone.utc)  
        
        # 然后使用用户 ID 获取推文
        tweets = client.get_users_tweets(
            id=user_id,
            max_results=100,
            exclude="retweets",
            start_time=start_time,
            end_time=end_time
        )
        
        if tweets.data:
            for tweet in tweets.data:
                print(tweet)
        else:
            print("No tweets found")
    else:
        print("User not found")
        
except tweepy.errors.Unauthorized as e:
    print(f"认证失败: {str(e)}")
except Exception as e:
    print(f"发生错误: {str(e)}")




import os
import tweepy
from dotenv import load_dotenv


class TwitterBot:
    def __init__(self, env_path=".env"):
        """
        Initialize Twitter bot with credentials from .env file
        """
        load_dotenv(env_path)  # Load environment variables

        # Validate required environment variables
        required_vars = [
            "API_KEY", "API_SECRET",
            "ACCESS_TOKEN", "ACCESS_TOKEN_SECRET"
        ]

        missing_vars = [var for var in required_vars if not os.getenv(var)]
        if missing_vars:
            raise ValueError(f"Missing environment variables: {', '.join(missing_vars)}")

        self.api = tweepy.Client(
            bearer_token=os.getenv("BEARER_TOKEN"),
            consumer_key=os.getenv("API_KEY"),
            consumer_secret=os.getenv("API_SECRET"),
            access_token=os.getenv("ACCESS_TOKEN"),
            access_token_secret=os.getenv("ACCESS_TOKEN_SECRET")
        )

    def post_tweet(self, text):
        """
        Post a tweet with the given text
        Returns tweet object if successful
        """
        try:
            tweet = self.api.create_tweet(text=text)
            print(f"Tweet posted successfully! ID: {tweet.data['id']}")
            return tweet
        except tweepy.TweepyException as e:
            print(f"Error posting tweet: {str(e)}")
            raise
        except Exception as e:
            print(f"Unexpected error: {str(e)}")
            raise

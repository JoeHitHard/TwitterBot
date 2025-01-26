from abc import ABC, abstractmethod

from twitter_bot import TwitterBot


class TwitterPostGenerator(ABC):
    """
    Abstract base class for generating and posting Twitter content
    """

    def __init__(self):
        """
        Initialize Twitter bot instance
        """
        self.bot = TwitterBot()

    @abstractmethod
    def generate_content(self, input_text: str) -> str:
        """
        Generate text content for the tweet (must be implemented by subclasses)
        """
        pass

    def validate_content(self, content: str) -> bool:
        """
        Validate tweet content before posting
        Returns True if valid, False otherwise
        """
        if len(content) > 280:
            print(f"Content too long ({len(content)} characters)")
            return False
        if not content.strip():
            print("Content cannot be empty")
            return False
        return True

    def post(self, input_text: str) -> bool:
        """
        Execute the full posting workflow:
        1. Generate content
        2. Validate content
        3. Post tweet
        Returns True if successful, False otherwise
        """
        try:
            content = self.generate_content(input_text)
            if not self.validate_content(content):
                return False
            self.bot.post_tweet(content)
            return True
        except Exception as e:
            print(f"Posting failed: {str(e)}")
            return False
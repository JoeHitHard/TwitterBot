import os
from dotenv import load_dotenv
from typing import Optional
from openai import OpenAI

from twitter_post_generator import TwitterPostGenerator


class CryptoAnalysisPoster(TwitterPostGenerator):
    """
    Generates and posts cryptocurrency technical analysis using DeepSeek's LLM
    """

    def __init__(self, token: str):
        super().__init__()
        self.token = token.upper()
        self.emoji_map = {
            "BTC": "₿",
            "ETH": "Ξ",
            "SOL": "◎",
            "DOT": "●",
            "ADA": "𝔸"
        }

    def _get_token_emoji(self) -> str:
        """Get relevant emoji for common cryptocurrencies"""
        return self.emoji_map.get(self.token, "🚀")

    def generate_content(self, input_text: str) -> Optional[str]:
        """
        Generate technical analysis using DeepSeek's API
        Returns formatted tweet content or None if generation fails
        """
        try:
            # Get raw analysis from LLM
            analysis = self._get_technical_analysis(input_text)

            if not analysis:
                return None

            # Format for Twitter
            return self._format_tweet(analysis)

        except Exception as e:
            print(f"Analysis generation failed: {str(e)}")
            return None

    def _get_technical_analysis(self, input_text: str) -> Optional[str]:
        """Make API call to DeepSeek's LLM"""
        try:

            client = OpenAI(
                api_key=os.getenv("DEEPSEEK_API_KEY"),
                base_url="https://api.deepseek.com"
            )

            prompt = f"""Provide concise technical analysis for {self.token} including:
            - RSI (3-5 word sentiment )
            - Key moving averages (5 words max)
            - MACD trend (3 words max)
            - Support/resistance levels (simple format)
            - Chart pattern observation
            - Buy/sell signals use ↓ or ↑
            - dont add number of characters
            - make it a human readable simple english paragraph
            IMPORTANT: Keep under 250 characters. Use crypto trading abbreviations.
            Latest CoinInfo: {input_text}"""

            response = client.chat.completions.create(
                model="deepseek-reasoner",
                messages=[
                    {"role": "system", "content": "You're a professional efficient crypto analyst."},
                    {"role": "user", "content": prompt},
                ],
                temperature=0.7,
                max_tokens=280
            )

            return response.choices[0].message.content.strip()

        except Exception as e:
            print(f"DeepSeek API Error: {str(e)}")
            return None

    def _format_tweet(self, analysis: str) -> str:
        """Format analysis into engaging tweet"""
        emoji = self._get_token_emoji()
        hashtags = f"#{self.token} #Crypto #TechnicalAnalysis"

        return (

            f"🤖Bot\n{emoji} {self.token} Technical Update {emoji}\n"
            f"{analysis}\n"
            f"By ChainSignal"
            # f"{hashtags}"
        )


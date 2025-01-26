import os

import requests
import json
from pprint import pprint

from dotenv import load_dotenv


class CryptoDataAnalyzer:
    def __init__(self, coin_id='bitcoin', api_key=None):
        self.coin_id = coin_id
        self.api_key = api_key
        self.base_url = f"https://api.coingecko.com/api/v3/coins/{self.coin_id}"
        self.headers = {
            "accept": "application/json",
        }
        if self.api_key:
            self.headers["x-cg-pro-api-key"] = self.api_key

    def fetch_data(self):
        """Fetch raw cryptocurrency data from CoinGecko API"""
        try:
            response = requests.get(self.base_url, headers=self.headers)
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            print(f"Request failed: {e}")
            return None

    @staticmethod
    def extract_info(data):
        """Extract and structure cryptocurrency information from raw data"""
        if not data:
            return None

        return {
            'basic_info': {
                'id': data.get('id'),
                'name': data.get('name'),
                'symbol': data.get('symbol'),
                'categories': data.get('categories', []),
                'genesis_date': data.get('genesis_date'),
                'market_cap_rank': data.get('market_cap_rank'),
            },
            'market_data': {
                'current_price_usd': data['market_data'].get('current_price', {"usd": 0}).get('usd', 0),
                'market_cap_usd': data['market_data'].get('market_cap', {"usd": 0}).get('usd', 0),
                'total_volume_usd': data['market_data'].get('total_volume', {"usd": 0}).get('usd', 0),
                'price_change_24h_usd': data['market_data'].get('price_change_24h_in_currency', {"usd": 0}).get('usd',
                                                                                                                0),
                'price_change_percentage': {
                    '24h': data['market_data'].get('price_change_percentage_24h'),
                    '7d': data['market_data'].get('price_change_percentage_7d'),
                    '30d': data['market_data'].get('price_change_percentage_30d'),
                    '1y': data['market_data'].get('price_change_percentage_1y'),
                },
                'all_time_high_usd': data['market_data'].get('ath', {"usd": 0}).get('usd', 0),
                'all_time_low_usd': data['market_data'].get('atl', {"usd": 0}).get('usd', 0),
                'supply': {
                    'circulating': data['market_data'].get('circulating_supply'),
                    'total': data['market_data'].get('total_supply'),
                    'max': data['market_data'].get('max_supply'),
                }
            },
            'community': {
                'twitter_followers': data['community_data'].get('twitter_followers'),
                'reddit_subscribers': data['community_data'].get('reddit_subscribers'),
                'sentiment': data.get('sentiment_votes_up_percentage'),
            },
            'development': {
                'github_stars': data['developer_data'].get('stars'),
                'github_forks': data['developer_data'].get('forks'),
                'recent_commits': data['developer_data'].get('commit_count_4_weeks'),
            },
            'exchange_data': sorted([
                {
                    'exchange': ticker['market']['name'],
                    'pair': f"{ticker['base']}/{ticker['target']}",
                    'last_price': ticker.get('last'),
                    'volume': ticker.get('converted_volume', {}).get('usd'),
                    'trust_score': ticker.get('trust_score'),
                    'spread': ticker.get('bid_ask_spread_percentage'),
                } for ticker in data.get('tickers', [])
            ], key=lambda x: x.get('volume', 0), reverse=True)[:5]
        }

    def generate_report(self, data, save_path=None):
        """Generate and display analysis report, optionally save to file"""
        if not data:
            print("No data to generate report")
            return

        print("Cryptocurrency Analysis Report:")

        if save_path:
            print("=" * 50)
            pprint(data, indent=2, depth=2, compact=False)
            print("=" * 50)
            with open(save_path, 'w') as f:
                json.dump(data, f, indent=2)
            print(f"\nReport saved to {save_path}")

    def analyze(self, save_path=None):
        """Complete analysis workflow: fetch, process, and report data"""
        raw_data = self.fetch_data()
        if not raw_data:
            return None

        processed_data = self.extract_info(raw_data)
        self.generate_report(processed_data, save_path)
        return processed_data


# Example usage
# if __name__ == "__main__":
#     load_dotenv()
#
#     analyzer = CryptoDataAnalyzer(
#         coin_id="bitcoin",
#         api_key=os.getenv("COIN_GECKO_API_KEY")
#     )
#
#     # Single method call for complete analysis
#     analysis_result = analyzer.analyze()
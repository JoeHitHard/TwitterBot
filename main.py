import json
import os

from dotenv import load_dotenv

from coin_data import CryptoDataAnalyzer
from deepseek_llm_crypo_analysis_generator import CryptoAnalysisPoster

if __name__ == "__main__":
    load_dotenv()
    analyzer = CryptoDataAnalyzer(
        coin_id="bitcoin",
        api_key=os.getenv("COIN_GECKO_API_KEY")
    )

    # Single method call for complete analysis
    analysis_result = analyzer.analyze()

    btc_poster = CryptoAnalysisPoster("BTC")
    content = btc_poster.generate_content(json.dumps(analysis_result))
    print(content)
    print(len(content))

    # btc_poster.post()

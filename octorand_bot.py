from datetime import datetime
from twitter_bot import TwitterBot
from tiny_monitor import TinyMonitor
import assets

twitter = TwitterBot()
octo_monitor = TinyMonitor(assets.OCTORAND)

time = datetime.now().strftime("%m/%d/%Y, %I:%M %p")
price = octo_monitor.get_asset_quote_price(per_algo=False)

twitter.send_tweet(f"{time}\nOctorand Price: {price:.02f}Ⱥ")
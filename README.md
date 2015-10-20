# tw_share2vk
Share tweets to vk by tag

### Usage
  1. Install requirements `pip install -r requirements.txt`
  2. Edit `tw_share2vk.py` and set `twtag = ""`
    - Example: `twtag = "PS4Share"`
  3. Set your own Twitter and VK apps secrets
    - Example: `https://oauth.vk.com/authorize?client_id=4513896&scope=wall,photos&redirect_uri=https://oauth.vk.com/blank.html&display=page&v=5.37&response_type=token`
  4. Add `tw_share2vk.py` to cron

import os          
import json

class ApiConfig():
    AREA_LIST_URL = "https://api.live.bilibili.com/room/v1/Area/getList"
    START_LIVE_URL = "https://api.live.bilibili.com/room/v1/Room/startLive"
    STOP_LIVE_URL = "https://api.live.bilibili.com/room/v1/Room/stopLive"
    QR_CODE_GENERAT_URL = "https://passport.bilibili.com/x/passport-login/web/qrcode/generate"
    QR_CODE_LOGIN_URL = "https://passport.bilibili.com/x/passport-login/web/qrcode/poll"

class HeadersConfig():
    HEADERS = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/115.0.0.0 Safari/537.36'
}

class LiveConfig():

    room_id = 0 
    area_v2	= 0
    platform = 'pc_link'

    is_configured = False

    cookies = {
        'SESSDATA': 'your_sessdata_value',
        'bili_jct': 'your_bili_jct_value',
    }

    def __init__(self):
        self.load_config()
        pass

    def load_config(self):
        if os.path.exists('config.json'):
            with open('config.json', 'r') as f:
                config = json.load(f)
                self.room_id = config.get('room_id', self.room_id)
                self.area_v2 = config.get('area_v2', self.area_v2)
                self.platform = config.get('platform', self.platform)
                self.cookies = config.get('cookies', self.cookies)
                self.is_configured = True
        else:
            print("未找到配置文件.")
            self.is_configured = False

    def save_config(self):
        config = {
            'room_id': self.room_id,
            'area_v2': self.area_v2,
            'cookies': self.cookies
        }
        with open('config.json', 'w') as f:
            json.dump(config, f, indent=4)
        print("Configuration saved to 'config.json'.")

    def set_config(self, room_id, area_v2, cookies):
        self.room_id = room_id
        self.area_v2 = area_v2
        self.cookies = cookies
        self.save_config()

    def print_config(self):
        print(f"Room ID: {self.room_id}")
        print(f"Area V2: {self.area_v2}")
        print(f"Platform: {self.platform}")
        print(f"Cookies: {self.cookies}")

if __name__ == "__main__":
    # 测试配置
    x = LiveConfig()
    print(x.room_id, x.area_v2, x.platform, x.cookies)
    pass
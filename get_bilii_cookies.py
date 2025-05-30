import requests
from qrcode import QRCode 
from config import LiveConfig, ApiConfig, HeadersConfig
import time

class BiliQRLogin():

    def __init__(self, 
                 qr_generate_url=ApiConfig.QR_CODE_GENERAT_URL,
                 login_url=ApiConfig.QR_CODE_LOGIN_URL,
                 headers=HeadersConfig.HEADERS):
        """
        初始化B站二维码登录器
        
        参数:
        qr_generate_url: 二维码生成API地址
        login_check_url: 登录状态检查API地址
        headers: 请求头配置
        """
        self.qr_generate_url = qr_generate_url
        self.login_url = login_url
        self.headers = headers
        self.cookies = None
        self.qr_key = None
        self.qr_url = None

    def generate_qr_code(self):
        """
        生成B站登录二维码
        """
        response = requests.get(self.qr_generate_url, headers=self.headers)

        response_json = response.json()

        if response.status_code == 200 and response_json.get('code') == 0:
            qr_code_data = response_json.get('data', {})
            self.qr_url = qr_code_data.get('url', '')
            self.qr_key = qr_code_data.get('qrcode_key', '')

            qr = QRCode(version=1, box_size=10, border=4)

            qr.add_data(self.qr_url)
            qr.make(fit=True)
            qr.print_ascii()  # Print QR code in ASCII format
            print("请使用B站APP扫码登录。")
        else:
            print(f"二维码生成失败: {response_json.get('message', 'Unknown error')}")

    def get_bilii_cookies(self, poll_interval=0):

            is_qrcode_scanned = False
            
            while True:
                poll_response = requests.get(self.login_url, params={'qrcode_key': self.qr_key}, headers=self.headers)
                poll_json = poll_response.json()

                if poll_response.status_code == 200 and poll_json.get('code') == 0:
                    data = poll_json.get('data', {})
                    code = data.get('code', 0)

                    if code == 0:
                        print("登录成功！")
                        self.cookies = poll_response.cookies.get_dict()
                        return self.cookies
                    elif code == 86038:
                        print("二维码已失效，请重新生成。")
                        return None
                    elif code == 86090:
                        if is_qrcode_scanned:
                            continue
                        print("扫码成功，请在B站APP上确认登录。")
                        is_qrcode_scanned = True
                        continue
                    elif code == 86101:
                        continue
                time.sleep(poll_interval)

def main():
    login = BiliQRLogin()
    login.generate_qr_code()
    cookies = login.get_bilii_cookies()
    print("获取到的Cookies:", cookies)
    pass
if __name__ == "__main__":
    main()
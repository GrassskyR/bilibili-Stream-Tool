import requests
import json
from config import ApiConfig, HeadersConfig, LiveConfig
from get_bilii_cookies import BiliQRLogin
import os
def start_stream():
    clear_screen()
    # Initialize configuration
    live_config = LiveConfig()
    if not live_config.is_configured:
        print("请先配置直播间信息。")
        return
    # Start live stream
    start_live_data = {
        'room_id': live_config.room_id,
        'area_v2': live_config.area_v2,
        'platform': live_config.platform,
        'csrf': live_config.cookies.get('bili_jct', ''),
    }
    
    response = requests.post(ApiConfig.START_LIVE_URL, data=start_live_data, headers=HeadersConfig.HEADERS, cookies=live_config.cookies)

    if response.status_code == 200:

        info = response.json()

        if info.get('code') == 0:
            
            if info.get('data', {}).get('change') == 1:
                print(f"开播成功 : 直播状态 {info.get('data', {}).get('status', 'Unknown')}")
            else:
                print("重复开播")

            rmtp_info = info.get('data', {}).get('rtmp', {})

            print(f"RTMP推流地址: {rmtp_info.get('addr', 'Unknown')}")
            print(f"RTMP推流码: {rmtp_info.get('code', 'Unknown')}")
            
        else:
            print(f"开播失败 : {info.get('message', 'Unknown error')}")

    else:
        print(f"请求失败: {response.status_code}, {response.text}")

    # print(response.status_code, response.text)

def close_stream():
    clear_screen()
    # Close live stream
    live_config = LiveConfig()

    if not live_config.is_configured:
        print("请先配置直播间信息。")
        return

    close_data = {
        'room_id': live_config.room_id,
        'csrf': live_config.cookies.get('bili_jct', ''),
    }
    
    response = requests.post(ApiConfig.STOP_LIVE_URL, data=close_data, headers=HeadersConfig.HEADERS, cookies=live_config.cookies)
    # print(response.status_code, response.text)

    if response.status_code == 200:

        info = response.json()

        if info.get('code') == 0:

            if info.get('data', {}).get('change') == 0:
                print("直播未开播或已关播")
            else:
                print(f"关播成功 : 直播状态 {info.get('data', {}).get('status', 'Unknown')}")
            
        else:
            print(f"关播失败 : {info.get('message', 'Unknown error')}")

    else:
        print(f"请求失败: {response.status_code}, {response.text}")

def configure_stream():
    clear_screen()
    live_config = LiveConfig()
    choice = 'n'

    if live_config.is_configured:
        print("直播信息已配置：")
        live_config.print_config()
        print("重新配置？(y/n)")
        choice = input().strip().lower()
        if choice != 'y':
            print("已取消配置。")
            return
    
    print("请输入直播间ID :")
    room_id = input().strip()

    while not room_id.isdigit():
        print("无效的直播间ID，请重新输入:")
        room_id = input().strip()

    print("请输入直播分区ID (Sub-Area ID):")
    area_v2 = input().strip()

    while not area_v2.isdigit():
        print("无效的分区ID，请重新输入:")
        area_v2 = input().strip()

    login = BiliQRLogin()
    login.generate_qr_code()
    cookies = login.get_bilii_cookies()

    while not cookies:
        print("获取Cookies失败，请重新扫码登录。")
        login.generate_qr_code()
        cookies = login.get_bilii_cookies()

    SESSDATA = cookies.get('SESSDATA', '')
    bili_jct = cookies.get('bili_jct', '')
    if not SESSDATA or not bili_jct:
        print("获取Cookies失败，请检查登录状态。")
        return
    
    cookies = {
        'SESSDATA': SESSDATA,
        'bili_jct': bili_jct,
    }

    live_config.set_config(room_id, area_v2, cookies)

def clear_screen():
    os.system('cls' if os.name == 'nt' else 'clear')

def main():

    while True:
        print("1. 开播")
        print("2. 关播")
        print("3. 配置直播间信息")
        print("4. 退出")

        choice = input("请选择操作: ").strip()

        if choice == '1':
            start_stream()
        elif choice == '2':
            close_stream()
        elif choice == '3':
            configure_stream()
        elif choice == '4':
            break
        else:
            print("无效的选择，请重新输入。")

if __name__ == "__main__":
    main()
    pass
import requests
from bs4 import BeautifulSoup
import gspread
from google.oauth2.service_account import Credentials
import time  #用於分批寫入的延遲

#Google Sheets 連線設定
credentials = Credentials.from_service_account_file(
    'YOUR_SECRET_KEY.json',
    scopes=["https://www.googleapis.com/auth/spreadsheets"]
)
gc = gspread.authorize(credentials)
spreadsheet_url = "https://docs.google.com/spreadsheets/d/YOUR_GOOGLE_SHEET"
worksheet_name = "語音學"
worksheet = gc.open_by_url(spreadsheet_url).worksheet(worksheet_name)

#目標網址
url = "https://ocw.nycu.edu.tw/?course_page=all-course%2Fcollege-of-humanities-and-social-sciences%2F%E8%AA%9E%E9%9F%B3%E5%AD%B8-%E9%9F%B3%E9%9F%BB%E5%AD%B8-phonetics-phonology-101%E5%AD%B8%E5%B9%B4%E5%BA%A6-%E5%A4%96%E5%9C%8B%E8%AA%9E%E6%96%87%E5%AD%B8%E7%B3%BB-%E8%B3%B4%E9%83%81%E9%9B%AF"

#添加Headers模擬瀏覽器請求
headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/118.0.0.0 Safari/537.36"
}

# 發送 HTTP 請求
response = requests.get(url, headers=headers)
response.encoding = 'utf-8'

if response.status_code == 200:
    soup = BeautifulSoup(response.text, "html.parser")

    # 提取課程名稱
    course_title_elem = soup.find("h3", class_="penci-ibox-title")
    course_title = course_title_elem.get_text(strip=True).replace('\xa0', ' ') if course_title_elem else "未找到課程名稱"

    # 提取授課單位與教師
    course_unit_elem = soup.find("td", bgcolor="#EEEEEE") 
    course_unit = course_unit_elem.get_text(strip=True).replace('\xa0', ' ') if course_unit_elem else "未找到授課單位與教師"

    # 提取課程單元列表和對應連結
    course_units = []
    base_url = "https://ocw.nycu.edu.tw"  # 基本 URL
    unit_sections = soup.find_all("td", class_="column-2")
    for section in unit_sections:
        unit_name = section.get_text(strip=True)
        link_tag = section.find_next("a")  # 找到包含連結的 <a> 標籤
        if link_tag and link_tag.get("href"):
            relative_url = link_tag["href"]  # 提取相對 URL
            unit_url = f"{base_url}{relative_url}"  # 補全為完整 URL
        else:
            unit_url = "未找到單元連結"
        #整理資料，將每個課程單元的資料儲存在字典
        course_units.append({
            "課程名稱": course_title,
            "授課單位與教師": f'陽交大 {course_unit}',
            "課程單元": unit_name,
            "課程網址": unit_url
        })

    # 分批新增到 Google Sheets
    batch_size = 5  #每次寫入的行數
    for i in range(0, len(course_units), batch_size):
        batch = course_units[i:i + batch_size]
        for unit in batch:
            new_row = [
                unit["課程名稱"],
                unit["授課單位與教師"],
                unit["課程單元"],
                unit["課程網址"]
            ]
            try:
                worksheet.append_row(new_row)
            except Exception as e:
                print(f"寫入失敗: {e}")
        # 加上延遲，避免 Google Sheets API 過載
        time.sleep(2)
    
    print("所有課程單元資料已成功新增至 Google Sheet！")
else:
    print(f"無法訪問目標網站，HTTP 狀態碼: {response.status_code}")

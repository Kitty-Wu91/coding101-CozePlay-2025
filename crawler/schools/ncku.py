import requests
from bs4 import BeautifulSoup
import gspread
from google.oauth2.service_account import Credentials
import time  # 用於分批寫入的延遲

# Google Sheets 連線設定
credentials = Credentials.from_service_account_file(
    'YOUR_SECRET_KEY.json',  
    scopes=["https://www.googleapis.com/auth/spreadsheets"]
)
gc = gspread.authorize(credentials)
spreadsheet_url = "https://docs.google.com/spreadsheets/d/YOUR_GOOGLE_SHEET"  
worksheet_name = "力學"  
worksheet = gc.open_by_url(spreadsheet_url).worksheet(worksheet_name)

# 目標網址
url = "https://i-ocw.ctld.ncku.edu.tw/site/course_content/b0RSRrSTRh8"

# 添加 Headers 模擬瀏覽器請求
headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/118.0.0.0 Safari/537.36"
}

# 發送 HTTP 請求
response = requests.get(url, headers=headers)
response.encoding = 'utf-8'

if response.status_code == 200:
    soup = BeautifulSoup(response.text, "html.parser")

    # 提取課程名稱
    course_title_elem = soup.find("b")  # 假設課程名稱位於 <b> 標籤中
    course_title = course_title_elem.get_text(strip=True) if course_title_elem else "未找到課程名稱"

    # 提取授課單位（假設在 class="content-text" 的 <div> 標籤內）
    course_unit_elem = soup.select_one("div.course-content-box h3:contains('課程教師') + div.content-text")
    course_unit = course_unit_elem.get_text(strip=True) if course_unit_elem else "未找到授課單位"


    
    # 提取課程單元與對應網址
    course_units = []
    unit_list = soup.select("div.video-list ul#video_list_ul li")  # 提取單元列表
    for unit in unit_list:
        unit_name_elem = unit.find("span", class_="video-name")
        unit_name = unit_name_elem.get_text(strip=True) if unit_name_elem else "未找到單元名稱"

        unit_url_elem = unit.find("a", class_="video-link")
        unit_url = unit_url_elem["data-video-link"] if unit_url_elem and "data-video-link" in unit_url_elem.attrs else "未找到單元網址"

        course_units.append({
            "課程名稱": course_title,
            "授課單位與教師": f'成大 {course_unit}',  
            "課程單元": unit_name,
            "課程網址": unit_url
        })

    # 分批新增到 Google Sheets
    batch_size = 5  # 每次寫入的行數
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

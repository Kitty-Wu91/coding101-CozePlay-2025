import requests
from bs4 import BeautifulSoup
import gspread
from google.oauth2.service_account import Credentials
import time  # 用於延遲

# Google Sheets 連線設定
credentials = Credentials.from_service_account_file(
    'YOUR_SECRET_KEY.json',  
    scopes=["https://www.googleapis.com/auth/spreadsheets"]
)
gc = gspread.authorize(credentials)
spreadsheet_url = "https://docs.google.com/spreadsheets/d/YOUR_GOOGLE_SHEET"
worksheet_name = "環境科學"
worksheet = gc.open_by_url(spreadsheet_url).worksheet(worksheet_name)

# 目標網址
url = "https://digital.nsysu.edu.tw/nvironmental_science-2/"  # 替換為實際課程網址

# 發送 HTTP 請求
response = requests.get(url)
response.encoding = 'utf-8'

if response.status_code == 200:
    #使用BeautifulSoup解析HTML
    soup = BeautifulSoup(response.text, "html.parser")

    # 1. 抓取課程名稱
    course_name_tag = soup.find('h2', class_="elementor-heading-title")
    course_name = course_name_tag.text.strip() if course_name_tag else "未找到課程名稱"

    # 2. 固定授課單位與教師
    professor_info = "環工所 袁中新  "  # 固定輸入內容

    # 3. 抓取課程單元與課程連結
    course_units = []
    units_section = soup.find_all('a', class_="list-group-item")
    for unit in units_section:
        unit_name = unit.text.strip()
        unit_link = unit.get('name', '').split("##")[0]  # 擷取連結部分
        course_units.append({
            "課程名稱": course_name,
            "授課單位與教師": f"中山 {professor_info} 教授",
            "課程單元": unit_name,
            "課程網址": unit_link
        })

    # 4. 批量新增到 Google Sheets
    try:
        rows_to_add = [
            [
                unit["課程名稱"],
                unit["授課單位與教師"],
                unit["課程單元"],
                unit["課程網址"]
            ]
            for unit in course_units
        ]
        # 每 50 行寫入一次，避免超過配額限制
        for i in range(0, len(rows_to_add), 50):
            worksheet.append_rows(rows_to_add[i:i + 50])
            time.sleep(10)  # 每批寫入後延遲 10 秒
        print("所有課程單元資料已成功新增至 Google Sheet！")
    except Exception as e:
        print(f"新增資料至 Google Sheets 時出現錯誤：{e}")
else:
    print(f"無法訪問目標網站，HTTP 狀態碼: {response.status_code}")

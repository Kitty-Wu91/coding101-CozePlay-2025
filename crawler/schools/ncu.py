import requests
from bs4 import BeautifulSoup
import gspread
from google.oauth2.service_account import Credentials
import time  # 用於加入延遲

# Google Sheets 連線設定
credentials = Credentials.from_service_account_file(
    'YOUR_SECRET_KEY.json',  # 替換為正確路徑
    scopes=["https://www.googleapis.com/auth/spreadsheets"]
)
gc = gspread.authorize(credentials)
spreadsheet_url = "https://docs.google.com/spreadsheets/d/YOUR_GOOGLE_SHEET"
worksheet_name = "微積分"
worksheet = gc.open_by_url(spreadsheet_url).worksheet(worksheet_name)

# 目標網址
url = "https://ocw.ncu.edu.tw/course/syllabus?courseId=423"
# 發送 HTTP 請求
response = requests.get(url)
response.encoding = 'utf-8'

if response.status_code == 200:
    # 使用 BeautifulSoup 解析 HTML
    soup = BeautifulSoup(response.text, "html.parser")

    # 抓取課程名稱
    course_name_tag = soup.find('dt', text="課程名稱")
    course_name = course_name_tag.find_next('dd').text.strip() if course_name_tag else "未找到課程名稱"

    # 抓取授課教師與單位
    professor_info = "未找到授課教師信息"
    paragraphs = soup.find_all('p')  # 尋找所有的 <p> 標籤
    for p in paragraphs:
        if "教授" in p.text:  # 檢查文字內容是否包含 "教授"
            professor_info = p.text.strip()
            break  # 找到後立即退出循環

    # 抓取課程單元
    course_units = []
    units_section = soup.find_all("div", class_="text")
    for unit in units_section:
        node_title = unit.find("div", class_="text-overflow")
        if node_title:
            unit_name = node_title.text.strip()
            course_units.append({
                "課程名稱": course_name,
                "授課單位與教師": f"中大 {professor_info}",
                "課程單元": unit_name,
                "課程網址": url  # 使用固定課程網址
            })

    # 批量新增到 Google Sheets
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

import requests
from bs4 import BeautifulSoup
import gspread
from google.oauth2.service_account import Credentials

# Google Sheets 連線設定
credentials = Credentials.from_service_account_file(
    'YOUR_SECRET_KEY.json',  
    scopes=["https://www.googleapis.com/auth/spreadsheets"]
)
gc = gspread.authorize(credentials)
spreadsheet_url = "https://docs.google.com/spreadsheets/d/YOUR_GOOGLE_SHEET"  
worksheet_name = "力學"  # 工作表名稱
worksheet = gc.open_by_url(spreadsheet_url).worksheet(worksheet_name)

# 目標網址
url = "https://cdtl.video.nchu.edu.tw/km/1367"  # 替換為您的課程網址

# 發送 HTTP 請求
response = requests.get(url)
response.encoding = 'utf-8'

# 檢查 HTTP 狀態碼
if response.status_code == 200:
    # 使用 BeautifulSoup 解析 HTML
    soup = BeautifulSoup(response.text, "html.parser")

    # 提取課程名稱
    course_title_div = soup.find("div", class_="title pull-left")
    course_title = course_title_div.get_text(strip=True) if course_title_div else "未找到課程名稱"

    # 提取授課教師
    teacher_name = "林立"  # 直接填入教師名稱

    # 提取課程單元
    course_units = []
    unit_sections = soup.find_all("div", class_="node-title")  # 調整選取器為 "node-title"
    if not unit_sections:
        print("未找到任何課程單元，請檢查選取器是否正確。")

    for section in unit_sections:
        # 提取單元名稱
        for child in section.find_all(["span", "div"], recursive=False):
            child.extract()
        unit_name = section.get_text(strip=True)

        # 提取單元連結編號
        link_tag = section.find_parent("a", href=True)  # 尋找最近的父級 <a> 標籤
        if link_tag:
            href = link_tag["href"]
            unit_id = href.split("/")[-1]  # 從連結提取 ID
            unit_url = f"https://cdtl.video.nchu.edu.tw/media/{unit_id}"
        else:
            unit_url = "未找到單元連結"

        # 儲存單元資料
        course_units.append({
            "課程名稱": course_title,
            "授課單位與教師": f"中興 {teacher_name} 教授",
            "課程單元": unit_name,
            "課程網址": unit_url
        })

    # 新增到 Google Sheets
    rows = [
        [unit["課程名稱"], unit["授課單位與教師"], unit["課程單元"], unit["課程網址"]]
        for unit in course_units
    ]
    try:
        if rows:
            worksheet.append_rows(rows)
            print("所有課程單元資料已成功新增至 Google Sheet！")
        else:
            print("未找到課程單元資料，無法新增。")
    except Exception as e:
        print(f"新增資料至 Google Sheet 時出現錯誤：{e}")

else:
    print(f"無法訪問目標網站，HTTP 狀態碼: {response.status_code}")

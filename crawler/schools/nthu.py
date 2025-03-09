import requests
from bs4 import BeautifulSoup
import gspread
from google.oauth2.service_account import Credentials

# Google Sheets 連線設定
credentials = Credentials.from_service_account_file(
    'YOUR_SECRET_KEY.json',  # 替換為正確路徑
    scopes=["https://www.googleapis.com/auth/spreadsheets"]
)
gc = gspread.authorize(credentials)
spreadsheet_url = "https://docs.google.com/spreadsheets/d/YOUR_GOOGLE_SHEET"
worksheet_name = "神經科學"
worksheet = gc.open_by_url(spreadsheet_url).worksheet(worksheet_name)

# 目標網址
url = "https://ocw.nthu.edu.tw/ocw/index.php?page=course&cid=261&"

# 發送 HTTP 請求
response = requests.get(url)
response.encoding = 'utf-8'

if response.status_code == 200:
    # 使用 BeautifulSoup 解析 HTML
    soup = BeautifulSoup(response.text, "html.parser")
    
    # 提取課程名稱
    course_title = soup.find("div", class_="section_title_area pera-content headline relative-position")
    course_title = course_title.find("h2").get_text(strip=True).replace('\xa0', ' ') if course_title and course_title.find("h2") else "未找到課程名稱"
    
    # 提取授課單位與教師
    course_unit = soup.find("div", class_="quote_text")
    course_unit = course_unit.find("h3").get_text(strip=True).replace('\xa0', ' ') if course_unit and course_unit.find("h3") else "未找到授課單位與教師"
    
    # 提取課程單元列表和對應的單元連結
    course_units = []
    unit_sections = soup.find("div", id="ocwChapters").find_all("a")  # 根據 HTML 結構提取單元連結
    for section in unit_sections:
        unit_name = section.get_text(strip=True)  # 單元名稱
        href = section.get("href")  # 提取連結
        if href:
            # 從連結中提取 `cid` 和 `chid`
            params = requests.utils.urlparse(href).query
            query_params = dict(x.split("=") for x in params.split("&"))
            cid = query_params.get("cid", "未知")
            chid = query_params.get("chid", "未知")
            unit_url = f"https://ocw.nthu.edu.tw/ocw/index.php?page=chapter&cid={cid}&chid={chid}"
            
            # 添加到單元資料中
            course_units.append({
                "課程名稱": course_title,
                "授課單位與教師": f'清大 {course_unit}',
                "課程單元": unit_name,
                "課程網址": unit_url
            })

    # 新增到 Google Sheets
    for unit in course_units:
        new_row = [
            unit["課程名稱"],
            unit["授課單位與教師"],
            unit["課程單元"],
            unit["課程網址"]
        ]
        worksheet.append_row(new_row)
    print("所有課程單元資料已成功新增至 Google Sheet！")
else:
    print(f"無法訪問目標網站，HTTP 狀態碼: {response.status_code}")


import requests
from bs4 import BeautifulSoup
import gspread
from google.oauth2.service_account import Credentials

# Google Sheets 連線設定
credentials = Credentials.from_service_account_file(
    'YOUR_SECRET_KEY.json',  # 替換為正確的 JSON 憑證檔案路徑
    scopes=["https://www.googleapis.com/auth/spreadsheets"]
)
gc = gspread.authorize(credentials)
spreadsheet_url = "https://docs.google.com/spreadsheets/d/YOUR_GOOGLE_SHEET"  # Google Sheet 的網址
worksheet_name = "微積分"  # 工作表名稱
worksheet = gc.open_by_url(spreadsheet_url).worksheet(worksheet_name)

# 目標網址
url = "http://www.math.ncu.edu.tw/~cchsiao/OCW/01.html"  # 替換為您的目標課程網址

# 發送 HTTP 請求
response = requests.get(url)
response.encoding = 'utf-8'

if response.status_code == 200:
    # 使用 BeautifulSoup 解析 HTML
    soup = BeautifulSoup(response.text, "html.parser")

    # 固定課程名稱與教師
    course_title = "微積分"
    teacher_name = "鄭經斅"

    # 提取課程單元
    course_units = []
    rows = soup.find_all("tr")  # 查找所有表格行
    for row in rows:
        # 使用 class 列表匹配方式
        columns = row.find_all("td", class_=["td02", "td03"])
        if len(columns) >= 3:  # 確保資料完整
            # 提取單元名稱
            unit_chapter = columns[0].get_text(strip=True)  # 章節名稱
            unit_title = columns[1].get_text(strip=True)  # 單元標題

            # 提取單元連結
            video_link_tag = columns[2].find("a", href=True)
            video_link = video_link_tag["href"] if video_link_tag else "未找到連結"

            # 儲存單元資料
            course_units.append({
                "課程名稱": course_title,
                "授課教師":  f"中大 數學系 {teacher_name} 教授",
                "課程單元": f"{unit_chapter} {unit_title}",
                "課程網址": video_link
            })

    # 新增到 Google Sheets
    rows_to_add = [
        [unit["課程名稱"], unit["授課教師"], unit["課程單元"], unit["課程網址"]]
        for unit in course_units
    ]
    try:
        # 確保資料完整，並新增到 Google Sheet
        if rows_to_add:
            worksheet.append_rows(rows_to_add)
            print("所有課程單元資料已成功新增至 Google Sheet！")
        else:
            print("未找到課程單元資料，無法新增。")
    except Exception as e:
        print(f"新增資料至 Google Sheet 時出現錯誤：{e}")

else:
    print(f"無法訪問目標網站，HTTP 狀態碼: {response.status_code}")

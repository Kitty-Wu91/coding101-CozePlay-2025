import requests
from bs4 import BeautifulSoup
import gspread
from google.oauth2.service_account import Credentials

#Google Sheets連線設定
credentials = Credentials.from_service_account_file(
    'YOUR_SECRET_KEY.json',
    scopes=["https://www.googleapis.com/auth/spreadsheets"]
)
gc = gspread.authorize(credentials) 
spreadsheet_url = "https://docs.google.com/spreadsheets/d/YOUR_GOOGLE_SHEET"

worksheet_name = "微積分"
worksheet = gc.open_by_url(spreadsheet_url).worksheet(worksheet_name)

#目標網址與基礎 URL
url = "https://ocw.aca.ntu.edu.tw/ntu-ocw/ocw/cou/100S111/1"
base_url = "https://ocw.aca.ntu.edu.tw/ntu-ocw/ocw/cou/100S111/"

#發送HTTP請求
try:
    response = requests.get(url, timeout=10)
    response.encoding = 'utf-8'
    response.raise_for_status()  # 確保返回的狀態碼是 200
except requests.exceptions.RequestException as e:
    print(f"無法訪問目標網站: {e}")
    exit()

# 使用 BeautifulSoup 解析 HTML
soup = BeautifulSoup(response.text, "html.parser")

def clean_text(text):
    """清理文本內容，處理空值和特殊字符"""
    return text.get_text(strip=True).replace('\xa0', ' ') if text else "未找到相關內容"

# 提取課程名稱與授課單位
course_title = clean_text(soup.find("h2", class_="title"))
course_unit = clean_text(soup.find("h4", class_="unit"))

# 提取課程單元列表
unit_sections = soup.find_all("div", class_="AccordionPanelTab-text")
if not unit_sections:
    print("未找到課程單元資料，請檢查目標網站結構。")
    exit()

# 整理課程資料
course_units = []
for idx, section in enumerate(unit_sections, start=1):  # 使用 enumerate 獲取單元編號（從 1 開始）
    unit_name = section.get_text(strip=True)  # 單元名稱
    unit_url = f"{base_url}{idx}"  # 對應的課程網址
    course_units.append({
        "課程名稱": course_title,
        "授課單位與教師": f'臺大 {course_unit}',
        "課程單元": unit_name,
        "課程網址": unit_url
    })

# 批量寫入 Google Sheets
rows = [
    [unit["課程名稱"], unit["授課單位與教師"], unit["課程單元"], unit["課程網址"]]
    for unit in course_units
]
worksheet.append_rows(rows)
print("所有課程單元資料已成功新增至 Google Sheet！")

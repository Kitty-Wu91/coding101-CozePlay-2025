# 📝 Coze 輔助功能工作流：摘要與擴寫 (`summarize_or_expand_workflow`)

---

## 1. 功能概述

本工作流提供 **「摘要」** 與 **「擴寫」** 兩種功能，幫助用戶快速獲取文章摘要，或將簡短內容擴展成更完整的段落。

📌 **主要目標**
- **摘要 (Summarization)**：擷取 **網頁內容**，透過 **大語言模型 (LLM)** 生成 **精簡摘要**
- **擴寫 (Expansion)**：根據 **用戶輸入**，讓 **LLM 進行補充與擴展**

📌 **工作流總覽圖**：
![輔助功能總覽](images/summarize_or_expand.png)

---

## 2. AI 技術應用

### **1️⃣ 大語言模型 (Large Language Model, LLM)**
   - **負責摘要**：將 **網頁內容** 壓縮為精簡摘要
   - **負責擴寫**：根據 **用戶輸入** 進行詳細擴展

---

## 3. 工作流程運作流程

以下為 **完整的 Coze 工作流步驟**，每個步驟都有說明與過程截圖：


### 1️⃣ **用戶選擇功能**
- **啟動工作流**，用戶選擇：
  - **「摘要」**
  - **「擴寫」**

📌 **工作流示意圖：**  
![用戶選擇功能](images/summarize_or_expand_1.png)

---

## **(A) 摘要流程**

### 2️⃣ **用戶輸入網址**
- **用戶提供目標文章的網址**
- 系統 **檢查網址格式是否正確**

📌 **工作流示意圖：**  
![用戶輸入網址](images/summarize_or_expand_2.png)

---

### 3️⃣ **將網址編碼**
- **轉換網址格式**，確保可用於查詢

📌 **工作流示意圖：**  
![網址編碼](images/summarize_or_expand_3.png)

---

### 4️⃣ **確認是否有歷史摘要**
- **查詢資料庫**，如果該網址 **已存在摘要**，則 **直接輸出結果**
- **若無資料**，則繼續擷取網頁內容

📌 **工作流示意圖：**  
![確認歷史摘要](images/summarize_or_expand_4.png)

---

### 5️⃣ **擷取網頁資訊**
- **抓取該網址的 HTML 內容**
- **解析出純文字內容**

📌 **工作流示意圖：**  
![擷取網頁內容](images/summarize_or_expand_5.png)

---

### 6️⃣ **LLM 生成摘要**
- **使用 LLM (`GPT-4o mini`)**，根據擷取的 **網頁內容** 生成摘要
- **確保摘要內容完整且精簡**

📌 **工作流示意圖：**  
![LLM 生成摘要](images/summarize_or_expand_6.png)

---

### 7️⃣ **儲存並輸出結果**
- **將摘要內容存入資料庫**
- **輸出摘要給用戶**

📌 **工作流示意圖：**  
![儲存並輸出摘要](images/summarize_or_expand_7.png)

---

## **(B) 擴寫流程**

### 8️⃣ **用戶輸入內容**
- **用戶提供簡短內容**
- 系統 **檢查輸入長度**，確保適合作為擴寫目標

📌 **工作流示意圖：**  
![用戶輸入擴寫內容](images/summarize_or_expand_8.png)

---

### 9️⃣ **LLM 進行擴寫**
- **使用 LLM (`GPT-4o mini`)**，根據用戶輸入 **補充額外資訊**
- 生成 **更完整的內容**
- **將擴寫內容顯示給用戶**

📌 **工作流示意圖：**  
![LLM 擴寫內容](images/summarize_or_expand_9.png)



# 🔎 Coze 輔助功能工作流：搜尋其他平台 (`yt_and_googlescholar_workflow`)
## 1. 功能概述

本工作流允許用戶選擇不同的搜尋平台來查詢相關內容，支援 **YouTube、Google Scholar 及 Google 搜尋**。

📌 **主要功能**：
- **YouTube 搜尋**：允許用戶輸入關鍵字，查詢 YouTube 影片
- **Google Scholar 搜尋**：支援輸入關鍵字與論文年份參數，查詢學術論文
- **Google 搜尋**：進行一般網頁搜尋

📌 **工作流總覽圖**：
![搜尋其他平台 - 總覽](images/search_overview.png)

---
## 2. 技術要點
1. **Coze 平台外掛整合**：
   - `search_video`（YouTube API）
   - `searchGoogleScholar`（Google Scholar API）
   - `googleWebSearch`（Google API）
2. **動態輸入處理**：
   - 允許用戶 **選擇不同搜尋平台**
   - 根據不同搜尋方式，**動態調整輸入參數**
3. **多通道資訊檢索**：
   - 依用戶需求搜尋 **影片、學術論文、或網頁資料**
   - **回傳最符合用戶需求的內容**

---

## 3. 工作流程運作流程

以下為 **完整的 Coze 工作流步驟**，每個步驟都有說明與過程截圖：

---

### 1️⃣ **用戶選擇搜尋類型**
- **使用 `Question` 節點**，詢問用戶希望搜尋的類型
- 提供選項：
  - **A：YouTube**
  - **B：Google Scholar**
  - **其他：Google 預設搜尋**

📌 **工作流示意圖：**
![選擇搜尋類型](images/search_step1.png)

---

### 2️⃣ **YouTube 搜尋**
- **用戶輸入關鍵字**
- **透過 `search_video` 外掛**，查詢 YouTube 影片
- **輸出搜尋結果**

📌 **工作流示意圖：**
![YouTube 搜尋](images/search_step2.png)

---

### 3️⃣ **Google Scholar 搜尋**
- **用戶輸入關鍵字**
- **可選擇性地輸入論文年份範圍**
- **透過 `searchGoogleScholar` 外掛**，查詢 Google Scholar 論文
- **輸出搜尋結果**

📌 **工作流示意圖：**
![Google Scholar 搜尋](images/search_step3.png)

---

### 4️⃣ **Google 搜尋**
- **用戶輸入關鍵字**
- **可選擇性地輸入最大回傳結果數**
- **透過 `googleWebSearch` 外掛**，執行 Google 搜尋
- **輸出搜尋結果**

📌 **工作流示意圖：**
![Google 搜尋](images/search_step4.png)

---

### 5️⃣ **結果輸出**
- **整合各搜尋來源的結果**
- **將搜尋結果返回給用戶**
- **工作流結束**

📌 **工作流示意圖：**
![搜尋結果輸出](images/search_step5.png)

---

# 🎯 Coze 主程式工作流 (`workflow_RAG`)

---

## ** 1. 主程式概述**
本專案透過 **Coze AI Agent開發平台**，建構一個 **基於檢索增強生成 (Retrieval-Augmented Generation, RAG)** 的學習課程推薦機器人。

### **📌 工作流的主要目標**
- **輸入解析**：使用 LLM 將用戶輸入翻譯為繁體中文，以利後續查詢
- **資料檢索**：透過 `Knowledge Retrieval` 插件，對課程摘要進行 **模糊搜尋 (Semantic Search)**，選取相關課程
- **LLM 組織輸出**：由 **大語言模型 (Large Language Model, LLM)** 生成 **概念解釋** 並整理推薦課程

📌 **工作流總覽圖**：
![Coze 主程式工作流](images/main_workflow.png)

---

## ** 2. AI 技術應用**
本系統主要應用了 **以下 AI 技術：**

### 1️⃣ **大語言模型 (Large Language Model, LLM)**
   - 用於 **翻譯用戶輸入**（翻譯成繁體中文）
   - 生成 **概念解釋**，幫助用戶理解查詢內容
   - 排序與整理推薦課程，確保最佳的結果呈現

### 2️⃣ **模糊搜尋 (Semantic Search)**
   - 透過 **Knowledge Retrieval**，使用 **向量相似度比對** 來進行 **語義檢索**
   - 可搜尋 **已建置的課程知識庫**，並選出 **最相關的課程摘要** 進行推薦

### 3️⃣ **檢索增強生成 (Retrieval-Augmented Generation, RAG)**
   - **融合 LLM + 知識庫檢索**，提高回應的準確度
   - 避免 LLM **「幻覺問題 (Hallucination)」**，確保回應內容與知識庫資料一致

---

## 3. 工作流程運作流程

以下為 **完整的 Coze 工作流步驟**，每個步驟都有說明與過程截圖：

---

### 🔷 1️⃣ **LLM 翻譯**
- **使用 LLM (`GPT-4o mini`)** 將用戶輸入內容翻譯成 **繁體中文**
- 這是為了確保與課程摘要的語言一致，提升檢索準確度

#### 📌 LLM 翻譯的 Prompt
```text
# 角色
你是一個翻譯專家。請將用戶輸入的文字翻譯成繁體中文。
如果沒有任何內容可翻譯，請直接輸出 {{user_input}}。
用戶輸入：{{user_input}}
# 請只輸出翻譯結果，不要加入其他解釋或內容。

# 📌 **工作流示意圖：**  
![LLM 翻譯](images/step1.png)

---

### 🔷 2️⃣ **Knowledge Retrieval 模糊搜尋**
- **使用 Knowledge Retrieval**，將用戶查詢與 **知識庫內的課程摘要** 進行 **語意比對**
- **檢索策略 (Search Strategy)**：`Semantic Search`
- **最多選取 15 筆** 相關課程作為候選清單

📌 **工作流示意圖：**  
![Knowledge Retrieval](coze_workflow/images/step2.png)

---

### 🔷 3️⃣ **LLM 生成課程推薦**
- **使用 LLM (`GPT-4o mini`)** 進一步篩選出 **相關度最高的 5 筆課程**
- **自動生成概念解釋**，幫助用戶理解查詢內容

#### 📌 LLM 整理輸出的 Prompt



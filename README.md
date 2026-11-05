# 人類圖共讀與研究手冊

整理人類圖共讀筆記、來源與反思提問，保留不同解讀及本人選擇。

**公會：人類圖研究所** · [自由工坊](https://freetwai.com) · [線上技能書](https://freetwai.com/development/skills/human-design)

## 模組說明 (Core Modules)

本專案包含以下核心模組與目錄：
- `scripts/validate.py`: 用於驗證研究筆記 JSON 檔案格式與資料結構的 Python 腳本。
- `templates/`: 存放共讀筆記、討論計畫與 JSON 格式的研究筆記等標準模板。
- `examples/`: 提供作為參考的全合成（非真實）人類圖共讀筆記範例。

## 開始使用 (Usage Examples)

1. 閱讀 [SKILL.md](SKILL.md)，選擇 `templates/` 目錄下的適當表格。
2. 參考 `examples/research-notes.json` 的全合成範例，填寫自己的工作副本。
3. 使用 `scripts/validate.py` 執行結構檢查，確認無誤後，再由實際負責人確認內容。

**執行驗證腳本：**
```sh
# 驗證 JSON 結構
python3 scripts/validate.py examples/research-notes.json
```
*預期輸出 (若成功):* `PASS: structural checks only; no real-world activity or results verified`

**執行測試：**
```sh
# 執行所有測試
python3 -m unittest discover -s tests -v
```

交付：一份附來源、不同觀點與匿名反思提問的共讀紀錄。

人類圖是供討論與自我反思的詮釋框架；本包不提供科學診斷、醫療建議、能力認證或職業配對。

## API 規格與資料結構 (API Specification)

`scripts/validate.py` 預期接收一個符合以下約束的 JSON 檔案：

- **`kind`** (字串, 必填): 必須為 `"human-design"`。
- **`title`** (字串, 必填): 研究筆記的標題，不能為空。
- **`data_classification`** (字串, 必填): 必須為 `"synthetic"` (公開範例僅接受合成資料)。
- **`consent_scope`** (字串, 必填): 同意聲明範圍，不能為空。
- **`birth_data_collected`** (布林值, 必填): 必須為 `false`，此範本不收集出生資料。
- **`sources`** (陣列, 必填): 包含至少一個來源物件，每個物件需有唯一 `id`、非空 `title` 與 `rights`，且 `url` 必須以 `https://` 開頭。
- **`notes`** (陣列, 必填): 包含至少一個筆記物件，每個物件必須有對應有效 `source_id`，且 `claim_type` 必須是 `interpretation`, `personal_observation`, `source_claim`, 或 `open_question` 之一。必須包含非空的 `summary`, `question`, `limitations` 欄位。

## 一起做

[待辦與里程碑](BACKLOG.md) · [認領與討論](https://github.com/FreeTWAI/freedom-skill-human-design/issues) · [目前 PR](https://github.com/FreeTWAI/freedom-skill-human-design/pulls) · [Fork](https://github.com/FreeTWAI/freedom-skill-human-design/fork)

Agent 先讀 [AGENTS.md](AGENTS.md)、[SKILL.md](SKILL.md) 與 [CONTRIBUTING.md](CONTRIBUTING.md)。待辦是可以提出認領的規劃；尚未分派，不代表已獲准或已完成。Issue 最新討論與 PR 是認領／審查紀錄。

```sh
python3 scripts/validate.py examples/research-notes.json
python3 -m unittest discover -s tests -v
```

只檢查資料結構與模板的已知約束，不代表真實活動、器材、研究或當事人同意已驗證。Python 3.10+，無第三方相依、無外部連線。

## 平台邊界

本倉維護原創手冊、模板與合成案例。會員、公會、權限與技能書綁定由 [freedom-platform](https://github.com/FreeTWAI/freedom-platform) 的 API／PostgreSQL 管理；本倉不能直接改中央資料庫。跨 repo 變更先連結相依 PR，不自行增加平台權限。公會會長未在此指定。

## 授權與來源

此包是自由工坊的原創入門內容，採 [MIT](LICENSE)。未複製第三方課程、圖表、媒體或設備軟體；外部素材必須保留各自權利與來源。`examples/` 均為合成資料，沒有已辦活動、真實客戶或研究成果的宣稱。

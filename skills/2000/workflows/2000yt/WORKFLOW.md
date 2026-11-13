# /2000yt

兩千／2000CAR 的 YouTube 內容優化入口，整合原 youtube-agent-skill 的 11 個流程與兩千封面製作，共 12 個子流程。接受 `/2000yt`、`$2000yt`、`/2000 yt`；英文子命令沿用 package、script、seo 等短名。

## 按需求選擇

| 調用 | 可辨識用詞 | 功能 | 按需讀取 |
| --- | --- | --- | --- |
| `/2000yt 封面` | 封面製作、封面標準、縮圖設計、thumbnail、cover | 品牌封面文案、版型、製作與檢查 | [流程](modules/yt-thumbnail/WORKFLOW.md) |
| `/2000yt 標題` | 標題、縮圖文案、title、package | 標題與縮圖配對，列出候選與取捨 | [流程](modules/yt-package/WORKFLOW.md) |
| `/2000yt 腳本` | 腳本、開場、hook | 開場候選與完整口播腳本 | [流程](modules/yt-script/WORKFLOW.md) |
| `/2000yt SEO` | SEO、說明欄、tags | 說明欄、標籤與搜尋意圖 | [流程](modules/yt-seo/WORKFLOW.md) |
| `/2000yt 熱門研究` | 熱門、爆款、viral | 依各頻道自身中位數辨識表現突出的影片 | [流程](modules/yt-viral/WORKFLOW.md) |
| `/2000yt 頻道健檢` | 健檢、頻道診斷、audit | 檢查頻道並指出最優先改善項目 | [流程](modules/yt-audit/WORKFLOW.md) |
| `/2000yt 留存` | 留存、觀眾流失、retention | 分析留存匯出資料與流失時間點 | [流程](modules/yt-retention/WORKFLOW.md) |
| `/2000yt 章節` | 章節、時間戳、chapters | 從逐字稿產生並檢查章節 | [流程](modules/yt-chapters/WORKFLOW.md) |
| `/2000yt 短片選段` | 短片、Shorts、選段 | 從長片逐字稿挑出可獨立成立的短片段落 | [流程](modules/yt-shorts/WORKFLOW.md) |
| `/2000yt 剪輯清單` | 剪輯清單、停頓、edit | 從逐字稿產生帶時間碼的刪剪建議 | [流程](modules/yt-edit/WORKFLOW.md) |
| `/2000yt 內容規劃` | 排程、內容規劃、plan | 依產能安排影片與短片題目 | [流程](modules/yt-plan/WORKFLOW.md) |
| `/2000yt 留言` | 留言、回覆、comment | 分類留言並草擬符合口吻的回覆 | [流程](modules/yt-comment/WORKFLOW.md) |

明確要求製作／審閱封面或整理封面標準時，選 thumbnail；只要標題／縮圖文案則選 package。「標題＋封面成品」可順序載入兩者。封面以兩千品牌標準為準，不套英文三單字上限。

有影片主題或原標題但未指定功能時，預設 package（標題＋縮圖）；只有 `/2000yt` 且無素材時，簡短告知已啟用，請使用者提供主題、原標題或影片。不要自動執行全部流程。

辨識舊名稱 yt-package、yt-script 等時，映射至上表對應子流程；載入該流程後，把裡面的 `/2000yt <英文名>` 視為本入口的子命令，不依賴舊獨立技能仍安裝。

## 共用規則

- 沿用本次對話中已確認的品牌口吻、素材、限制與授權。可讀取 `~/.codex/youtube/voice.md`；缺少時先用既有兩千品牌資料或使用者提供的範例，不因檔案不存在而重問已知資訊。只有口吻資訊確實不足時，才索取影片或文字範例。
- 預設用繁體中文，尊重使用者另指定的語言與風格。不捏造車況、價格、成果、數據或來源；標題承諾必須有內容支持。
- 原始工具主要使用英文斷詞與英文公式。中文標題的重複詞、模糊詞、前置詞與開場評分只能作有限參考，直接檢查中文語意；字元數也不等於畫面顯示寬度。任何分數都不是 CTR 或流量預測。
- 原流程的固定候選數、字數與顯示門檻是起點；使用者當次指定優先。需要試稿時提供可選候選與具體理由，不套用固定英文結尾。
- 這套流程產出文案、分析、封面成品與剪輯建議。實際製作／剪輯影片時依現有影片技能路由；長片品牌剪輯可接 `/2000 shorts`，已有成品要上架／排播可接 `/2000 reels`。需要建立完整頻道標題目錄或讀指定影片逐字稿時，可按需使用現有 youtube-channel-intelligence。不要因使用本技能而自動發布、回覆留言或修改外部文件。

## 路徑與執行

各 `modules/yt-*/` 是該子流程根目錄。腳本及 hooks.json 的同層／相鄰引用仍以該目錄為準；不要從最外層 2000 執行相對腳本路徑。六個 Python 工具及 21 個開場公式一併保留。

使用當前環境可用的 Python 3，執行時加 `-X utf8`。腳本路徑相對於對應子流程目錄，不依賴特定使用者的本機 runtime。

## 來源

改編自 [Jakeschincariol/youtube-agent-skill](https://github.com/Jakeschincariol/youtube-agent-skill)，版本 `a2feb2104981a375ffd4f87ee04f4f5344ac43c6`。保留 [MIT 授權](references/upstream-MIT.txt)。原 11 個流程調整入口、命名、路由及 Codex 使用說明；另新增依 22 張實際封面整理的兩千封面製作流程。工具程式與 hooks.json 維持原版。

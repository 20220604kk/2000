---
name: "2000"
description: "兩千／2000CAR 與馬尾技能的統一入口。使用者說 /2000、2000技能、舊的2000技能名稱或馬尾模式／健檢／審查／技術債時，選取對應工作流程；只載入本次需要的流程。"
---

# /2000

將 7 個兩千內容製作流程與 6 個馬尾流程整合到同一技能。接受 `$2000` 明確調用，也辨認使用者直接寫的 `/2000 <功能>` 與舊技能名稱。`/2000` 是顯示名稱及對話入口，不宣稱新增了宿主原生 slash command。

## 選擇流程

| 調用範例 | 功能 | 按需讀取 |
| --- | --- | --- |
| `/2000 blog` | 影片轉官網草稿 | [流程](workflows/2000blog/WORKFLOW.md) |
| `/2000 shorts` | Podcast 短影音剪輯 | [流程](workflows/2000car-podcast-shorts/WORKFLOW.md) |
| `/2000 cargogo` | 汽車介紹研究稿 | [流程](workflows/2000cargogo/WORKFLOW.md) |
| `/2000 podcast` | Podcast 完整集製作 | [流程](workflows/2000podcast/WORKFLOW.md) |
| `/2000 reels` | 四平台短影音排播 | [流程](workflows/2000reels/WORKFLOW.md) |
| `/2000 week` | 每週直播備題與封面 | [流程](workflows/2000week/WORKFLOW.md) |
| `/2000 writing` | 品牌文章寫作 | [流程](workflows/2000writing/WORKFLOW.md) |
| `/2000 馬尾` | 馬尾精簡開發 | [流程](workflows/ponytail/WORKFLOW.md) |
| `/2000 馬尾健檢` | 馬尾全專案健檢 | [流程](workflows/ponytail-audit/WORKFLOW.md) |
| `/2000 馬尾技術債` | 馬尾技術債 | [流程](workflows/ponytail-debt/WORKFLOW.md) |
| `/2000 馬尾效益` | 馬尾效益說明 | [流程](workflows/ponytail-gain/WORKFLOW.md) |
| `/2000 馬尾說明` | 馬尾操作說明 | [流程](workflows/ponytail-help/WORKFLOW.md) |
| `/2000 馬尾審查` | 馬尾變更審查 | [流程](workflows/ponytail-review/WORKFLOW.md) |

只讀對應的 WORKFLOW.md，再按該文連結讀必要參考。沒有指定功能時，簡短列出功能並請使用者選擇，不自動啟動所有流程。舊名稱如 2000reels、2000podcast、ponytail-review 均映射至上表。

短影音「剪輯」用 shorts；已有成品要「上架／排播」用 reels。影片轉文章用 blog；其他品牌文章用 writing。單次馬尾審查／健檢／技術債／效益／說明不自動開啟持續開發模式。馬尾模式接受 lite／full／ultra／off，預設 full；使用者取消後立即停止。

## 路徑與執行

每個 workflows/<舊名稱>/ 是原流程根目錄；其中 scripts/ 和 references/ 都相對於該目錄，不能相對於最外層 2000 執行。跨流程引用以同層 workflows 路徑讀取，不要求舊技能仍分別安裝。呼叫流程提到的其他技能時，先確認當前環境可用；缺少必要剪輯、文件或瀏覽器工具時明確說明，不宣稱本包已包含那些工具。

沿用當次已確認的素材、帳號、目的地、授權與進度，不套用歷史批次日期。建立／修改／分享技能不等於執行上架、文件寫入或影片製作。維護者與使用者的新指示優先於舊流程。

公開版的資源設定說明見 [references/environment.md](references/environment.md)。若本機已有相同設定，直接核對並使用；不要重問已知資訊。所有發布與不可逆聲明依當次任務授權處理。

馬尾來源：[DietrichGebert/ponytail](https://github.com/DietrichGebert/ponytail)，[MIT 授權](references/ponytail-MIT.txt)。

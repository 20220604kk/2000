# /2000

兩千／2000CAR 的內容製作與精簡開發技能，整合 14 項主流程；YouTube 優化另含 12 個子流程。提供 `2000` 統一入口與 `2000yt` YouTube 快捷入口。

## 使用

Codex 的明確技能調用是 `$2000` 或 `$2000yt`；本包顯示名稱為 `/2000`，也辨認對話中輸入的 `/2000 reels`、`/2000` 等文字。沒有安裝額外原生 slash command。

| 調用 | 功能 | 用意 |
| --- | --- | --- |
| `/2000 yt`／`/2000yt` | YouTube 優化 | 標題、品牌封面、腳本、SEO、熱門研究與頻道分析，詳見下表。 |
| `/2000 blog` | 影片轉官網草稿 | 把已確認的 YouTube 影片整理成含圖片、逐字稿與 SEO 的官網文章草稿。 |
| `/2000 shorts` | Podcast 短影音剪輯 | 從 Podcast 長片挑選精彩對話，剪成符合品牌版型的直式短影音。 |
| `/2000 cargogo` | 汽車介紹研究稿 | 查證車款規格、行情與競品，整理成主持人拍片時可直接使用的文稿。 |
| `/2000 podcast` | Podcast 完整集製作 | 完成雙機同步、剪輯、字幕、影音輸出，以及本集封面和 YouTube 資訊。 |
| `/2000 reels` | 四平台短影音排播 | 篩選已剪好的影片，以相同標題、封面與時間排程到 TikTok、YT、FB、IG。 |
| `/2000 week` | 每週直播備題與封面 | 整理當週話題與事故素材、更新直播文件，並製作封面。 |
| `/2000 writing` | 品牌文章寫作 | 撰寫或修改汽車與中古車文章，維持兩千品牌的口吻與編輯風格。 |
| `/2000` | 精簡開發 | 用最少但完整的修改完成開發任務，避免不必要的功能與複雜設計。 |
| `/2000 健檢` | 全專案健檢 | 檢查整個專案的錯誤、風險、效能與冗餘，列出優先改善項目。 |
| `/2000 技術債` | 技術債 | 找出程式中標記的暫時做法，整理限制與需要改善的時機。 |
| `/2000 效益` | 效益說明 | 說明可查證的效益與測量依據；沒有真實對照時不捏造節省數字。 |
| `/2000 說明` | 操作說明 | 查看全部功能、調用方式，以及開發模式的切換與關閉方法。 |
| `/2000 審查` | 變更審查 | 針對這次程式修改找出問題與風險，提出具體修正建議。 |

`/2000` 預設啟用精簡開發；`/2000 lite|full|ultra` 切換模式，`/2000 off` 停用。`/2000 說明` 顯示功能選單。

## YouTube 的 12 個子流程

`/2000yt` 與 `/2000 yt` 為相同入口。已有主題或原標題、未指定子功能時，預設產出標題與縮圖文案配對。

| 調用 | 功能 |
| --- | --- |
| `/2000yt 封面` | 品牌封面文案、版型、製作與檢查；包含 22 張參考封面與製作標準。 |
| `/2000yt 標題` | 標題與縮圖文案配對、候選比較。 |
| `/2000yt 腳本` | 開場設計與完整口播腳本。 |
| `/2000yt SEO` | 說明欄、標籤與搜尋意圖。 |
| `/2000yt 熱門研究` | 依各頻道自身表現基準找出突出的影片。 |
| `/2000yt 頻道健檢` | 頻道診斷與優先改善項目。 |
| `/2000yt 留存` | 分析留存匯出資料與流失時間點。 |
| `/2000yt 章節` | 從逐字稿產生並檢查時間戳章節。 |
| `/2000yt 短片選段` | 從長片逐字稿挑出可獨立成立的短片段落。 |
| `/2000yt 剪輯清單` | 產生帶時間碼的刪剪建議。 |
| `/2000yt 內容規劃` | 依產能安排長片與短片題目。 |
| `/2000yt 留言` | 分類留言並草擬符合口吻的回覆。 |

短片選段提供建議，實際剪輯使用 `/2000 shorts`；已有成品要上架或排播使用 `/2000 reels`。所有評分只作編輯參考，不是 CTR 或流量預測；不會自動發布影片或回覆留言。

## 安裝

將本儲存庫 `skills/2000` 與 `skills/2000yt` 兩個完整資料夾複製到同一個 Codex 技能目錄，例如 `~/.agents/skills/`。`2000yt` 會引用相鄰的 `2000`，不能單獨安裝；只安裝 `2000` 仍可透過 `/2000 yt` 使用 YouTube 流程。保留所有子目錄與參考圖片，只複製 SKILL.md 會遺失完整流程。

Windows PowerShell（先在本儲存庫目錄執行；目標已有 2000 或 2000yt 時先備份，不直接覆寫）：

```powershell
$skillRoot = Join-Path $env:USERPROFILE '.agents/skills'
foreach ($skillName in @('2000', '2000yt')) {
    if (Test-Path -LiteralPath (Join-Path $skillRoot $skillName)) {
        throw "$skillName 已存在，請先備份並移出舊版，再安裝。"
    }
}
New-Item -ItemType Directory -Force $skillRoot | Out-Null
Copy-Item -Recurse -LiteralPath './skills/2000' -Destination $skillRoot
Copy-Item -Recurse -LiteralPath './skills/2000yt' -Destination $skillRoot
```

安裝後重新開啟技能清單；若尚未出現，重啟 Codex。既有的 2000reels、2000podcast 等名稱在統一入口中仍可辨認。避免同時安裝相同流程的多份版本。

## 資源與適用範圍

公開的是可重用流程和檢查腳本。原影片、PSD、字型、音樂、剪映個人預設、私人文件連結、平台登入資料、後台識別碼、歷史任務紀錄均未打包。請按 [環境說明](skills/2000/references/environment.md) 指定自己的合法資源與目的地。此包不是一鍵剪輯引擎，也不自動授權網站發布或不可逆聲明。

Reels 使用三個網站、四個發布端點：TikTok、YouTube Shorts、Facebook Reels、Instagram。排程規則為台北每天 18:00／20:00，跳過週六 20:00；TikTok 最終審核版本為跨平台共用資料，Meta 保留 FB＋IG，不漏掉 IG。

## 來源與 MIT 授權

開發與審查流程改編自 [DietrichGebert/ponytail](https://github.com/DietrichGebert/ponytail)，保留原作者的 [MIT 授權全文](THIRD_PARTY_LICENSES/upstream-MIT.txt)。本包將流程整合為 `/2000`，調整指令、目錄與操作說明。其餘 2000CAR 流程的公開不另授予品牌、影音或母版使用權；未另外聲明的內容保留權利。

YouTube 原 11 個優化流程改編自 [Jakeschincariol/youtube-agent-skill](https://github.com/Jakeschincariol/youtube-agent-skill)，版本 `a2feb2104981a375ffd4f87ee04f4f5344ac43c6`，保留其 [MIT 授權全文](THIRD_PARTY_LICENSES/youtube-agent-skill-MIT.txt)。另加兩千品牌封面製作流程；22 張封面供品牌視覺參考，未另授予圖片、肖像或商標的使用權。

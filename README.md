# /2000

兩千／2000CAR 的內容製作與馬尾開發技能，整合成一個可安裝的 Codex skill，內含 13 項工作流程。繁體中文內容流程，保留馬尾開發／審查核心規則。

## 使用

Codex 的明確技能調用是 `$2000`；本包顯示名稱為 `/2000`，也辨認對話中輸入的 `/2000 reels`、`/2000 馬尾` 等文字。沒有安裝額外原生 slash command。

| 調用 | 功能 |
| --- | --- |
| `/2000 blog` | 影片轉官網草稿 |
| `/2000 shorts` | Podcast 短影音剪輯 |
| `/2000 cargogo` | 汽車介紹研究稿 |
| `/2000 podcast` | Podcast 完整集製作 |
| `/2000 reels` | 四平台短影音排播 |
| `/2000 week` | 每週直播備題與封面 |
| `/2000 writing` | 品牌文章寫作 |
| `/2000 ` | 精簡開發 |
| `/2000 健檢` | 全專案健檢 |
| `/2000 技術債` | 技術債 |
| `/2000 效益` | 效益說明 |
| `/2000 說明` | 操作說明 |
| `/2000 審查` | 變更審查 |

## 安裝

將本儲存庫 `skills/2000` 整個資料夾複製到自己的 Codex 技能目錄，例如 `~/.agents/skills/2000`。保留 workflows、references、scripts 子目錄；只複製 SKILL.md 會遺失完整流程。

Windows PowerShell（先在本儲存庫目錄執行；目標已有 2000 時先備份，不直接覆寫）：

```powershell
New-Item -ItemType Directory -Force "$env:USERPROFILE/.agents/skills" | Out-Null
Copy-Item -Recurse ./skills/2000 "$env:USERPROFILE/.agents/skills/2000"
```

安裝後重新開啟技能清單；若尚未出現，重啟 Codex。既有的 2000reels、2000podcast 等名稱在統一入口中仍可辨認。避免同時安裝相同流程的多份版本。

## 資源與適用範圍

公開的是可重用流程和檢查腳本。原影片、PSD、字型、音樂、剪映個人預設、私人文件連結、平台登入資料、後台識別碼、歷史任務紀錄均未打包。請按 [環境說明](skills/2000/references/environment.md) 指定自己的合法資源與目的地。此包不是一鍵剪輯引擎，也不自動授權網站發布或不可逆聲明。

Reels 使用三個網站、四個發布端點：TikTok、YouTube Shorts、Facebook Reels、Instagram。排程規則為台北每天 18:00／20:00，跳過週六 20:00；TikTok 最終審核版本為跨平台共用資料，Meta 保留 FB＋IG，不漏掉 IG。

## 來源與授權

馬尾工作流程改編自 [DietrichGebert/ponytail](https://github.com/DietrichGebert/ponytail)，保留原作者 [MIT 授權](THIRD_PARTY_LICENSES/ponytail-MIT.txt)。本包調整為統一入口、繁體中文索引，刪去未附帶的 host band／外掛設定，效益入口要求實際來源而不預設重現 benchmark。其餘 2000CAR 流程的公開不另授予品牌、影音或母版使用權；未另外聲明的內容保留權利。

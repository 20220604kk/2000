# 帳號與當批共用清單

## 已核實目標（2026-11-03）

| 端點 | 帳號 | 管理入口／識別 |
| --- | --- | --- |
| TikTok | `@2000car` | `https://www.tiktok.com/tiktokstudio/content`；由頭像選單的個人資料連結核對 handle |
| YouTube | 兩千的中古車-日榮汽車；管理員 | `https://studio.youtube.com/channel/UCotv4m6wWLlcP8RZsKEJAlA` |
| Facebook | 兩千中古車Youtube頻道 | Business `META_BUSINESS_ID`；asset `FACEBOOK_ASSET_ID` |
| Instagram | `@2000usedcar` | 與上述粉專同一 Meta Business Suite；建立 Reel 保留雙平台 |

Meta 入口：`https://business.facebook.com/latest/home?business_id=META_BUSINESS_ID&asset_id=FACEBOOK_ASSET_ID`。以上識別用來核對，不代表未來登入仍有效；使用者明確更換帳號時，以當次指示為準。

## 素材與規則

來源通常是 `<MEDIA_ROOT>\公用\<指定月份>`，通過資料在同月 `排播`。十月這次實際為 `10月`，不能把此名稱或 11 支數量當成固定值。每支通常含 MOV 與 `-封面.jpg`，也可能有 SRT。

台北固定時段為每天 18:00、20:00，跳過週六 20:00。起始日依當次要求；「今天下一個可用時段」按當時台北時間計算。先檢查目標帳號已有排程與本機紀錄，避免同素材重傳或占用已確認時段。

## 紀錄結構與恢復

每批建立本機工作目錄，保存 `shared-publishing-manifest.json`，至少包含：

- `timezone: Asia/Taipei`、`expectedVideos`、`expectedPlatformTasks`。
- `items[]`：穩定素材名稱、來源絕對路徑、大小、SHA-256、封面路徑、TikTok 審核後標題、帶 `+08:00` 的 `scheduledAt`、保存的隨機順序。
- `platforms.tiktok/youtube/facebook/instagram`：狀態、最終標題與時間、帳號、ID／管理網址、封面上傳結果、網站驗證與成功證據檔名。

狀態區分未上傳、傳輸中、草稿、已提交待確認、已接受待列表驗證、`scheduled`。成功一筆就寫回；整批 `complete` 只在四端點皆已驗證後記錄。`scheduled` 是平台接受未來排程，不代表影片已公開。

續作先讀清單，再檢查現有分頁和列表。分頁不在時重開管理頁核對；已有草稿直接續填，結果不明先查列表。不能把 setFiles 或暫存 promise 的完成當成網站排程成功。


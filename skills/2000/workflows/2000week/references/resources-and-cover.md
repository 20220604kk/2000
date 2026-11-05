# 固定資源與已驗證操作

## 直播文件

- 文件：固定 - 直播小話題整理
- URL：DOCUMENT_URL_FROM_USER
- document ID：`DOCUMENT_ID_FROM_USER`
- 已知tab：`t.0`；每次讀取確認。
- 2026/10/21排版：標題20pt、題目HEADING_1／18pt、內文及連結15pt、日期／來源12pt，多數題目一頁一題。以最新Doc人工調整為準。
- 開場範例：https://tsuyatt.com/games/wall-flip/ 。這是該週指定，不是每週必換或必用。

## 封面母版

`<MEDIA_ROOT>\網站素材\20250331 直播\封面設計\週三直播封面設計-已修復.psd`

2026/10/21已驗證992×558（16:9）；SHA256：`f8531525f03e7170f45d07341513a27d3f05cf64298fb1c59dfa8e49c23cf226`。以後母版變更就重新檢視，不直接當成錯誤。

| 用途 | 原圖層名／文字 | 處理 |
|---|---|---|
| 主標 | MG ZS | 改本週主標；字型jf-openhuninn-2.1，沿用白字黑框黃外框 |
| 日期 | 20260930 | 改直播日YYYYMMDD；字型AdobeFanHeitiStd-Bold |
| 固定提示 | 本日主題： | 保留 |
| 節目名 | 兩千の直播夜車 | 保留 |
| 節目時間 | 【每周三19:00】 | 保留，除非使用者改時間 |

隱藏的舊新聞清單及舊素材不要重新顯示。沿用主持人、道路背景與黃框；不要因Podcast母版是1920×1080就改這份模板尺寸。

## 輸出與操作

預設：`<MEDIA_ROOT>\網站素材\20250331 直播\封面設計\每週輸出\YYYYMMDD`，日期用實際直播日。遇同名成品先辨識版本，必要時放v2子資料夾，不盲目覆蓋。

- `YYYYMMDD_直播封面.png`
- `YYYYMMDD_直播封面.psd`
- `YYYYMMDD_直播封面_320x180.jpg`（檢查縮圖）
- `YYYYMMDD_封面檢查.json`、`YYYYMMDD_交付清單.json`

從技能目錄執行，將主標／日期／位置改為當次內容：

```powershell
& '.\scripts\build_cover.ps1' -Title '本週已確認主標' -Date8 'YYYYMMDD' -OutputDir '本週絕對輸出路徑' -Template '本次母版絕對路徑'
```

腳本以Photoshop COM讀取母版副本，保留可編輯字與樣式，主標放右側、日期放右上；只縮小過大主標，不改文字。短標過小或長標不適合時，看圖後調字級／區域再另存版本。已實測Photoshop 27.11.0；不能強制關閉使用者程式或文件。缺字型時先找原字型，若只能改用替代方式，交付須說明，不冒稱完全沿用。

用load_workspace_dependencies找本機Python；verify_cover.py需要Pillow與psd-tools。本機已可用的psd-tools位於 `<LOCAL_WORKSPACE>`，可透過參數提供：

```text
python scripts/verify_cover.py --template "母版路徑" --psd "本週PSD" --png "本週PNG" --title "本週主標" --date YYYYMMDD --psd-tools-dir "可用psd-tools資料夾"
```

腳本通過後仍須看原尺寸及縮圖。2026/10/21主標「中壢霸凌」、日期20261021已以母版原生字成功輸出，僅作案例，不是下週預設。

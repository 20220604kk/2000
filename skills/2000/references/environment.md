# 環境與資源

這個技能提供流程與檢查腳本，不包含原影片、PSD、音樂、字型、剪映預設、登入資料或帳號權限。公開版不含私人文件連結、後台 business/asset ID、歷史任務截圖與進度。

- `<MEDIA_ROOT>`：使用者提供的媒體根目錄；例如其下的 PODCAST、月份／排播資料夾。
- `<WORK_ROOT>`／`<LOCAL_WORKSPACE>`：本次可寫工作目錄；先確認存在與權限。
- `DOCUMENT_URL_FROM_USER`／`DOCUMENT_ID_FROM_USER`：使用者指定的 Google 文件；不把範例當輸出目的地。
- `META_BUSINESS_ID`／`FACEBOOK_ASSET_ID`：當前登入管理頁核實的目的地，不猜測。
- Reels：核對 TikTok、YouTube、FB、IG 四個帳號；Facebook＋Instagram 兩邊排程都設定。
- Podcast：先指定片頭、片尾、底 BAR PSD、封面 PSD、參考草稿與本集媒體。
- Week：先指定本週文件與封面母版；公開版腳本的 `-Template` 為必要參數。

Markdown 中的尖括號值是說明用佔位，執行命令前必須換成實際路徑。Podcast 初始化工具以環境變數 `CAR2000_MEDIA_ROOT` 選擇參考資源根目錄；未設定時採本次 `media_dir`，產生後仍逐一核對 references。不要把自動產生的路徑當成已驗證素材。

執行 Python 腳本需要 Python 3；媒體檢查需 FFmpeg／ffprobe；封面另需可用的 Photoshop、Pillow、psd-tools 與使用者有權使用的母版／字型。需要的相依工具按本次流程準備，本包不會自動安裝或啟動第三方服務。

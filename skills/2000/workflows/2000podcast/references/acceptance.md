# 25項驗收與100%門檻

EP157為版型／製作做法參考；各集機位、長度、聲音、調色與提問題數按實際內容驗收，不能做畫素相似度評分。

|ID|要求及有效證據|
|---|---|
|01|畫布與交付規格：1920×1080，成品60fps及正確音訊規格。|
|02|雙機、隱藏SRT、主BAR、諮商室底圖、提問、兩層進場、A1角色及覆蓋順序完整。|
|03|V1=A在右、V2=B在左，原始機位和人物已確認。|
|04|線性遮罩方向、羽化及中心接縫正確。|
|05|所有B分檔的本集構圖、遮罩、調色一致且適合本集。|
|06|B分檔完整連續覆蓋正式節目；接點無錯檔、非預期凍結、缺口、重疊或來源超界。|
|07|A/B/錄音在頭中尾、每個B來源與接點兩側同步；可信殘差在40ms內且無明顯唇形誤差。|
|08|相機原音關閉，不與主錄音重播。|
|09|節目使用獨立錄音，廣告／片尾聲音正確且只出現一次，gain有紀錄。|
|10|正式節目起訖正確，開頭與結尾音樂保留，來源時間碼有紀錄。|
|11|指定片頭廣告的素材、時長、聲音正確。|
|12|指定片尾影片的素材、時長、聲音正確。|
|13|片頭→節目→片尾的影音連續，總長一致，沒有意外空段。|
|14|正確底BAR PSD、本集集數／標題、畫面區透明。|
|15|底BAR覆蓋正式節目，諮商室可正常覆蓋主BAR。|
|16|正式節目逐字稿存在，排除外加廣告／片尾，所有字幕位於正式節目。|
|17|UTF-8 SRT序號、文字、時碼、起訖及順序有效，無意外重疊，與最新草稿字幕逐段相符。|
|18|台灣繁體、已確認人名／暱稱及專有名詞一致，保留校訂依據；不宣稱逐句零錯字。|
|19|SRT草稿軌隱藏；實際完成帶無壓逐字字幕、無字幕資料流，CC檔獨立可用。|
|20|「我的預設24」底圖、進場圖與角標完整，無缺漏資產。|
|21|依本集音樂／SRT定位諮商室，圖層與淡入淡出起訖正確。|
|22|本集全部提問替換，題數、時點、內容、字體、縮放、換行與邊界正確，無舊題。|
|23|已看最終交付影片的實際畫面：曝光膚色、裁切、接縫、每個B來源及提問均正常。|
|24|完整逐字稿逐句聽校；只有當次使用者明確豁免才記為waived，不能冒充pass。|
|25|實際完整帶輸出與影音檢查：全片解碼／畫格數、黑幀／凍結判讀、影音同步、峰值、頭尾音樂、動畫、無壓CC及版本一致。|

第24項只有當次使用者明確同意才可豁免；保存日期與原話，不繼承本包整理者的歷史授權。不得自行豁免其他項目。

## 報告結構

`init_episode.py`建立25項pending記錄。實際執行後填入每項 `status`（pass／fail／pending／waived）及具體 `evidence`。24獲當次明確授權豁免時，記錄實際內容（下列為結構示例）：

```json
"waivers": {"24": {"approved_by": "user", "date": "實際授權日期", "reason": "本次使用者明確豁免的原話"}}
```

本版門檻報告使用 `schema_version: 2`，包含：

- `episode`、25個唯一ID的 `checks`、適用的 `waivers`。
- `artifact_roles`：`draft_snapshot`、`video`、`audio`、`cc`、`lower_bar`、`cover_template` 對應到實際絕對路徑。
- `artifacts_sha256`：上述全部檔案以及本次驗收涵蓋素材的「絕對路徑→SHA256」。大媒體逐塊讀取。
- `actual_export_semantically_matches_latest_draft: true`：完成最新原生草稿語意比對後才填true；檢查器不會解密剪映或代做此比較。
- `reviews`：未豁免的23、24、25各自包含 `approved: true`、非空 `evidence_files`、`evidence_sha256` 及與主報告完全相同的 `artifacts_sha256`。看過實際影像／執行檢查才簽核。
- `video_evidence`：`visual_review`、`integrity`、`camera_sync`、`audio_sync` 四個JSON檔案的實際路徑，都須出現在對應review的evidence_files與evidence_sha256。

證據內容沿用本機已驗證的結構：

|證據|必要欄位|
|---|---|
|visual_review|approved=true、cc_not_burned_in=true、reviewed_file=實際MP4路徑，以及具體觀察與抽查截圖|
|integrity|decode_errors=false、all_output_frames_decoded=expected_frames>0、subtitle_stream_count=0、mp4_probe及mp3_probe、編碼後峰值分析、黑畫面／凍結判讀|
|camera_sync|JSON列陣；每筆含camera（A或B）、source_residual_seconds，以及來源／時間／匹配可信度；每機至少頭中尾3處，實際還須覆蓋每個B來源和接點|
|audio_sync|JSON列陣；每筆含file（mp4或mp3）、residual_seconds、correlation；兩種成品各至少3個有效時點，實際含廣告／節目／諮商室／片尾|

檢查器會驗證25項狀態、合法豁免、角色檔案及新鮮hash、review簽核與證據hash、主要JSON量測和格式。它不會證明人真的看過畫面、不會判斷假造的量測、不會自動把pending改成pass，也不取代原生草稿語意比較。

```text
python scripts/check_gate.py "<集數>_完整性檢查.json" --output "<工作目錄>\gate-result.json"
```

回傳碼0才開啟封面階段；2表示未通過。`recorded_pass_percent`只是記錄中的通過比例，`verified_percent`只有所有版本與證據通過才是100，否則為null，避免舊狀態仍顯示100%。

## 封面與最終交付另驗

影片門檻不預先要求不存在的封面，避免循環依賴。100%後完成封面，再寫封面視覺簽核與完整交付清單；不要把封面新增到影片hash表後直接保留舊review。

交付清單最少包含每個最終檔的path、bytes與sha256，包含MP4、MP3、封面PNG、YT資訊、SRT。封面簽核另記成品hash、原尺寸／縮圖、選圖時碼、母版保護及SRT主題依據。內容或素材改動後重做受影響檢查，不能只重算hash來繼承舊結論。

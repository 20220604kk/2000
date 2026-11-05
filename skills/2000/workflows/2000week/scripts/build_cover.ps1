param(
    [Parameter(Mandatory=$true)][string]$Title,
    [Parameter(Mandatory=$true)][ValidatePattern('^[0-9]{8}$')][string]$Date8,
    [Parameter(Mandatory=$true)][string]$OutputDir,
    [Parameter(Mandatory=$true)][string]$Template,
    [string]$TitleLayer = 'MG ZS',
    [string]$DateLayer = '20260930'
)
$ErrorActionPreference = 'Stop'
$sourceItem = Get-Item -LiteralPath $Template
$outPath = [IO.Path]::GetFullPath($OutputDir)
New-Item -ItemType Directory -Path $outPath -Force | Out-Null
$psdPath = Join-Path $outPath ($Date8 + '_直播封面.psd')
$pngPath = Join-Path $outPath ($Date8 + '_直播封面.png')
$reportPath = Join-Path $outPath ($Date8 + '_封面檢查.json')
if ((Test-Path -LiteralPath $psdPath) -or (Test-Path -LiteralPath $pngPath)) { throw 'Output exists. Inspect it and choose a new output directory or version before rerunning.' }
$beforeHash = (Get-FileHash -LiteralPath $Template -Algorithm SHA256).Hash
Copy-Item -LiteralPath $sourceItem.FullName -Destination $psdPath
$cfg = @{title=$Title; date=$Date8; psd=$psdPath; png=$pngPath; report=$reportPath; titleLayer=$TitleLayer; dateLayer=$DateLayer} | ConvertTo-Json -Compress
$jsx = @'
function quote(s) { return '"'+String(s).replace(/\\/g,'\\\\').replace(/"/g,'\\"').replace(/\r/g,'\\r').replace(/\n/g,'\\n')+'"'; }
function encode(x) {
 if(x===null) return 'null';
 if(typeof x==='string') return quote(x);
 if(typeof x==='number'||typeof x==='boolean') return String(x);
 var a=[], k;
 if(x instanceof Array) {for(k=0;k<x.length;k++)a.push(encode(x[k]));return '['+a.join(',')+']';}
 for(k in x) if(x.hasOwnProperty(k))a.push(quote(k)+':'+encode(x[k]));return '{'+a.join(',')+'}';
}
function findLayer(layers,name) {
 for(var i=0;i<layers.length;i++) {
  if(layers[i].name===name)return layers[i];
  if(layers[i].typename==='LayerSet'){var result=findLayer(layers[i].layers,name);if(result)return result;}
 }
 return null;
}
function bounds(l){var b=l.bounds;return [b[0].as('px'),b[1].as('px'),b[2].as('px'),b[3].as('px')];}
function fitLayer(l,box){
 var b=bounds(l),w=b[2]-b[0],h=b[3]-b[1],factor=Math.min(1,(box[2]-box[0])/w,(box[3]-box[1])/h);
 if(factor<1)l.resize(factor*100,factor*100,AnchorPosition.MIDDLECENTER);
 b=bounds(l);l.translate(UnitValue((box[0]+box[2]-b[0]-b[2])/2,'px'),UnitValue((box[1]+box[3]-b[1]-b[3])/2,'px'));
}
var oldDialogs=app.displayDialogs, oldUnits=app.preferences.rulerUnits,doc=null,result;
try {
 app.displayDialogs=DialogModes.NO;app.preferences.rulerUnits=Units.PIXELS;
 for(var j=0;j<app.documents.length;j++)try{if(app.documents[j].fullName.fsName===File(config.psd).fsName)throw Error('Output is already open.');}catch(e){if(String(e).indexOf('already open')>=0)throw e;}
 doc=app.open(File(config.psd));
 var title=findLayer(doc.layers,config.titleLayer),date=findLayer(doc.layers,config.dateLayer);
 if(!title||!date||title.kind!==LayerKind.TEXT||date.kind!==LayerKind.TEXT)throw Error('Expected editable title/date layers were not found.');
 var titleFont=title.textItem.font,dateFont=date.textItem.font,fontFound=false;
 for(var fi=0;fi<app.fonts.length;fi++)if(app.fonts[fi].postScriptName===titleFont)fontFound=true;
 if(!fontFound)throw Error('Template title font is not installed: '+titleFont);
 var before={title:title.textItem.contents,date:date.textItem.contents,titleBounds:bounds(title),dateBounds:bounds(date),titleFont:titleFont,dateFont:dateFont};
 title.textItem.contents=config.title;title.name=config.title;title.visible=true;
 fitLayer(title,[410,155,950,315]);
 date.textItem.contents=config.date;date.name=config.date;
 fitLayer(date,[856,3,981,29]);
 var psdOptions=new PhotoshopSaveOptions();psdOptions.layers=true;psdOptions.embedColorProfile=true;psdOptions.maximizeCompatibility=true;
 doc.saveAs(File(config.psd),psdOptions,false,Extension.LOWERCASE);
 var pngOptions=new PNGSaveOptions();pngOptions.interlaced=false;
 doc.saveAs(File(config.png),pngOptions,true,Extension.LOWERCASE);
 result={title:config.title,date:config.date,width:doc.width.as('px'),height:doc.height.as('px'),before:before,titleBounds:bounds(title),dateBounds:bounds(date),titleFont:title.textItem.font,dateFont:date.textItem.font,editableTitle:true,editableDate:true,psd:config.psd,png:config.png};
 var f=File(config.report);f.encoding='UTF8';f.open('w');f.write(encode(result));f.close();
 doc.close(SaveOptions.DONOTSAVECHANGES);doc=null;
} finally {
 if(doc)doc.close(SaveOptions.DONOTSAVECHANGES);
 app.preferences.rulerUnits=oldUnits;app.displayDialogs=oldDialogs;
}
encode(result);
'@
$weekPs = New-Object -ComObject Photoshop.Application
Get-Process Photoshop -ErrorAction SilentlyContinue | ForEach-Object { $_.PriorityClass = 'BelowNormal' }
$answer = $weekPs.DoJavaScript(('var config = ' + $cfg + ';' + [Environment]::NewLine + $jsx))
$afterHash = (Get-FileHash -LiteralPath $Template -Algorithm SHA256).Hash
if ($beforeHash -ne $afterHash) { throw 'Template fingerprint changed.' }
if (-not (Test-Path -LiteralPath $pngPath)) { throw 'PNG was not created.' }
$report = Get-Content -LiteralPath $reportPath -Raw -Encoding UTF8 | ConvertFrom-Json
$report | Add-Member NoteProperty template $sourceItem.FullName
$report | Add-Member NoteProperty templateSha256 $beforeHash
$report | Add-Member NoteProperty templateUnchanged $true
$report | ConvertTo-Json -Depth 20 | Set-Content -LiteralPath $reportPath -Encoding UTF8
Write-Output $answer

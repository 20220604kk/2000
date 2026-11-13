# /2000yt package

The title and the thumbnail are ONE unit. Writing them separately is why most packaging fails: the
thumbnail repeats the title, and half the click surface says the same thing twice.

```bash
python3 title.py --title "..." --thumb "AI RAN IT"
python3 title.py titles.txt            # one per line, ranked
```

## 兩千品牌封面

為 2000CAR 撰寫縮圖文案時，讀取 [兩千封面製作標準](../yt-thumbnail/references/production-standard.md)。中文封面遵循品牌的主標／副標層級，不套英文三個單字上限。需要實際製作圖片時轉入 `/2000yt 封面`；只要標題與文案時不自動生成圖片。

## Before you write

1. Read `~/.codex/youtube/voice.md` if it exists. That is the user's voice profile: how they talk
   on camera, the words they never use, who they are talking to, what they will not claim. If it
   does not exist, ask for **three of their own videos**, read or transcribe them, infer the voice,
   and write the file. A script in the wrong voice is worse than no script, because they have to
   read it out loud.
2. Never invent a number, a result or a source. If a figure would strengthen it and you do not have
   one, ask for it or write the line without it.

## Rules the tool enforces, and why

- **60 characters** is where desktop search truncates, **40** is a mobile home feed. Both are
  reported because they fail differently: a desktop cut loses the tail, a mobile cut can lose the
  subject.
- **The thumbnail complements the title.** Share necessary car names or figures, but do not paste the entire title onto the image.
- **Use the brand text hierarchy.** For 2000CAR Chinese thumbnails, follow the linked production standard and verify readability at reduced size.
- **A number, a name or a date** beats every adjective available to you.
- **Two all-caps words is the ceiling** before a title reads as spam.

## Write ten, keep two

Generate ten titles, run them all through `title.py`, show the user the top three with their scores
and the specific issue on each. For the winner, write the thumbnail brief: the expression, the
framing, the three words, and what the background has to do to hold contrast at feed size.

## The gate

Nothing here publishes. This skill writes and you publish. Every output ends in a block the user
copies, and the last line of every run is the question: **ship it, or change it?**

## Local Codex runtime

Use a working Python 3 interpreter in the current environment. Resolve script paths relative to this module directory, and run Python with `-X utf8` for UTF-8 input and output.

The bundled title.py uses English tokenization. For Chinese titles, explain that its word-overlap, filler-word and vagueness scores are unreliable; judge the Chinese wording directly. Its score is a heuristic, not a CTR prediction.

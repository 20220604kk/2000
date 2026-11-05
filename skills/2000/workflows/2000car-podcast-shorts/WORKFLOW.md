# 2000CAR Podcast Shorts

Apply this skill as the brand/editorial layer on top of the available video-editing workflow. The user's newest explicit instructions always override these defaults.

Before selecting shots or designing text, read [references/brand-spec.md](references/brand-spec.md). For a full cut, recut, render, or delivery pass, also read [references/production-workflow.md](references/production-workflow.md).

## Core outcome

Produce fast social hooks that make viewers curious about the long episode without finishing the story. When the user says to reuse the EP.150 format and gives no new quantity or runtime, default to six separate 13-second vertical clips. Each clip must contain an audible conversational handoff, not a single-speaker monologue.

Keep source files untouched. Put working files, transcripts, EDLs, QA images, and outputs under the episode's `edit/` directory. Resume decisions from `edit/project.md` and append the current session after delivery.

## Non-negotiable editorial rules

- Treat 兩千 as the protagonist, 阿嘎 as support, and off-camera 阿宏 as lowest priority.
- Keep 兩千 visually dominant in every clip; use 阿嘎 for concise answers or punchlines and reduce 阿宏 to the minimum context required for coherence.
- Center the displayed person. Do not leave the face biased toward either edge.
- Keep music at a fixed low level. Do not sidechain, duck, or automatically avoid speech unless the user reverses this preference.
- Preserve an unresolved question, contradiction, incomplete explanation, or reaction that motivates a click to the full episode.
- Burn captions last, after every graphic overlay.

## Delivery checks

For the established 13-second format, verify 1080×1920, 60 fps, exactly 780 video frames, 13.000 seconds, complete decode, readable titles at phone scale, and synchronized captions after every discontinuous cut. Run `scripts/validate_outputs.py` on the delivery directory; use `--loudness` when final audio has been normalized.

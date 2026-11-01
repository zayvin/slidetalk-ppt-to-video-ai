# Course video without re-recording: turn your lecture slides into a sellable course

Recording a 30-lesson course the traditional way means: prep the script, set up lighting, screen-record, restart whenever you fluff a line, cut the coughs out, hand-time the captions, export, upload. Three to five hours per lesson, two or three months for the course. The worst part is that **changing one slide means re-recording a whole lesson** — a textbook update, a data refresh, a different instructor, and it all starts again.

With SlideTalk the deck stays a deck, the script lives in the app, and you fix the page you need to fix. Regenerate that page's voiceover and the rest is untouched.

## Who this is for

- **Paid-course authors** whose course has to sell for two years and therefore has to be cheap to update
- **University lecturers and training providers** who teach the same course every term with small changes
- **Corporate trainers** handed a deck by the business and asked to make it watchable
- **Anyone selling the same course in a second language**

## The settings that matter

| Setting | Recommended | Why |
| --- | --- | --- |
| Input | **PDF** for chart-heavy decks, **PPTX** for text decks | PDF reproduces layout exactly; charts never shift |
| Narration mode | **Solo** for lectures; **teacher–student Q&A** for tutorials | Q&A has a built-in rhythm that monologue lacks |
| Voice | Lecturer/education, 1.0x–1.1x | Clear articulation, no rising endings — survives long listening |
| Target platform | **YouTube** or **podcast** (long-form specs) | Sets aspect ratio, cover ratio and title length |
| Brief | Say who is watching, what they already know, what they should be able to do afterwards | Drives terminology density |
| Splits | One split point per chapter, export as separate videos | Chapters become sellable units and are easy to revise |

## What a 30-lesson course actually costs

| | Traditional recording | SlideTalk |
| --- | --- | --- |
| Per lesson | 3–5 hours | 20–40 minutes including review |
| 30 lessons | 90–150 hours (2–3 months) | 10–20 hours (2–3 days) |
| Changing one slide | Re-record the lesson | Edit that page's script, regenerate its voiceover |
| A second language | Record everything again | Re-brief the script in the target language, switch voice |
| Captions | Hand-timed or third-party ASR plus cleanup | Burned in automatically, plus a sidecar `.srt` |
| AI cost | 0 (but labour is the cost) | ~352 credits ≈ US$0.50 per ten-slide video |

These are order-of-magnitude figures that depend on how fast you review. The real difference is **rework cost**: traditional recording punishes every change, SlideTalk charges you for one page.

## Three things that make a series work

**1. Sell chapters, not one long file**
Do not export a 40-minute monolith from a 30-slide deck. Put a split point on each chapter's first slide and export five or six 8-minute videos, each with its own cover and title. They can be sold individually, reordered, or replaced without touching the rest. When splitting, you can repeat the previous segment's last slide for continuity so the cut does not feel abrupt.

**2. The first fifteen seconds decide completion rate**
Do not open with "Hi everyone, today we're looking at chapter three". Open with a concrete question: "Why does your model score 99% in training and fall apart in production?" AI drafts usually open with the first version — rewrite it.

**3. Do not translate a bilingual edition, rewrite it**
A bilingual script is not a sentence-by-sentence translation. Chinese naturally says "we look at this chart first"; English is more natural as "look at the dip in week three". When generating the English edition, write the brief in English ("explain to US undergraduates why training accuracy is misleading") and you get prose written in English, not translated into it.

## Common traps

- **Slide text is too small.** On a phone, body copy under 24pt is mush. Fixing the deck is cheaper than fixing the video.
- **Eight bullets per slide.** A video is not a handout. Two or three points per slide; split the rest into new pages. The "concise" narration style helps, but density is your call.
- **Equations and code.** PDF input is the most reliable. With PPTX, export those pages as images and place them yourself.
- **Native animations.** PowerPoint animations are not inherited. Use the six built-in scene animations for emphasis — they align to the narration, which PowerPoint transitions never do.
- **The instructor's own voice.** If "taught by a named expert" is the product, an AI voice weakens trust. Keep the real recording and use the app for captions and covers.

## Pre-publish checklist

Run through the [pre-publish checklist](../templates/export-checklist.md), and specifically:

1. Every slide's script can actually be read aloud — long sentences, brackets and symbols break first
2. The voice is consistent across the whole course
3. Captions never cover the number a chart is making
4. Chapter timestamps match the content
5. The cover is legible as a thumbnail on a phone

## Next

- [Download SlideTalk](https://apps.apple.com/us/app/slidetalk-ppt-to-video-ai/id6800015747), then run the [sample lesson](../examples/chart-lesson/README.md) end to end
- Full script-writing method: [speaker notes into a voiceover script](../handbook/narration-and-speaker-notes.md)
- Comparing options: [four approaches](../compare/ppt-to-video-tools.md)

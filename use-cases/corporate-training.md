# Corporate training and product demos: turn a deck into a standard course video

The expensive thing inside a company is not making a video. It is **delivering the same thing over and over**: the same onboarding deck for twenty cohorts a year, the same product demo re-told by every solutions engineer with slightly different words, the same compliance training that everyone must complete and someone must be able to prove.

Turn the deck into a video once and everyone sees the same version. What usually blocks that decision is three worries — **can the material leave the network, will the content go stale, and what about other languages**. Here is each, in order.

## Worry 1: does the deck have to be uploaded?

No. SlideTalk renders video with Apple's AVFoundation **on the machine**, with nothing uploaded and nothing queued. Project files, slide images, scripts, audio and finished cuts stay in the app's sandbox container and are deleted when the app is uninstalled.

Only AI generation needs a network, and it sends very little:

| Step | What leaves the device | What does not |
| --- | --- | --- |
| Script generation | That slide's text, plus the slide image if visual understanding is on | Other slides, the original file, your history |
| Voiceover | The text to be read | Slide content, images |
| Cover | The title copy and the style brief | Deck content |

The gateway does not store user content. **If the deck contains unreleased financials or customer lists, turn visual understanding off, or replace those pages with placeholders before importing** — that advice is tool-independent common sense.

## Worry 2: what happens when content goes stale?

This is the biggest hidden cost in corporate training: a policy changes, a product ships, and every video is obsolete.

Because the video maps one-to-one onto the deck, updates are local:

1. Open the project and go to that page
2. Edit the script (or edit the deck and re-import that page)
3. Regenerate only that page's voiceover and animations
4. Re-render and export

No re-recording, no re-editing. A 40-page compliance course with three changed policies takes about twenty minutes.

## Worry 3: what about other languages?

Same deck, script regenerated in the target language, different voice — an English course. Japanese, Korean and the rest work the same way. The voice library has more than a hundred voices across lecturer, business, warm and trending styles.

One caveat: **do not translate sentence by sentence**. Re-brief the content in the target language ("explain to new hires in the US why we log every access request") and you get prose written in that language rather than translated prose.

## Settings for common corporate scenarios

| Scenario | Mode | Voice | Platform | Note |
| --- | --- | --- | --- | --- |
| Onboarding | Solo | Business/broadcast, steady and clear | YouTube / podcast specs | 40 pages into 5 chapters, exported separately |
| Product demo | Solo or two-person | Warm + business | YouTube | Two-person mimics "customer asks, SE answers" |
| Compliance | Solo | Business/broadcast | Podcast / internal specs | 0.95x speed, captions always on |
| Manager training | Teacher–student | Lecturer/education | YouTube | Q&A suits abstract discussion better |
| Support scripts | Two-person | Warm × 2 | Vertical | 9:16 for phone-sized learning |

## A standard production process

The corporate risk is that every video looks different. Fix a template first, then produce in batches:

1. **Fix the cover template.** Brand colour, logo position, title size. The Publish Center outputs per-platform covers; pick one template and stop changing it.
2. **Fix the opening line.** Same first ten seconds across the series ("This is lesson 3 of the X series") so learners feel continuity.
3. **Fix the voice.** One voice for the whole series at one speed. Changing voice damages consistency more than changing the cover.
4. **Fix the chapter rule.** One chapter every 5–8 pages, named as "verb + object" ("Configure access permissions", not "Part three").
5. **Fix the review checklist.** Below.

## Pre-publish checklist (corporate)

- [ ] Sensitive data redacted — customer names, unreleased financials, internal hostnames
- [ ] Every figure has a source and a date
- [ ] Compliance statement at the top of the video or first line of the description
- [ ] Voice, speed and cover template match the rest of the series
- [ ] Captions do not cover the key chart
- [ ] Chapter timestamps match the content
- [ ] Export resolution matches the internal player (1080p is a common ceiling)
- [ ] File name follows the internal convention (`dept_series_lesson_version_date`)

## What it costs

| Item | Charge |
| --- | --- |
| Import, editing, audition, render, export | Free (480p–4K, no length limit) |
| AI script | 1 credit per slide |
| AI voiceover | 1 credit per 10 characters |
| AI cover | 80 credits per image |
| AI title / description / tags | 2 credits per run |
| A 10-slide video | ≈ 352 credits ≈ US$0.50 |

A 40-page course with full AI assets lands around US$2. Against outsourced production (priced per finished minute, often hundreds to thousands), the gap is an order of magnitude. **Note** this is AI cost, not your time — the real saving is not re-recording.

## Before procurement

- **Platforms:** Mac (macOS 15.1+), iPhone and iPad (iOS/iPadOS 17+). **No Windows build** — a Windows-only team needs a Mac or an iPad.
- **Accounts:** no registration; the app uses Apple's AppTransaction for an anonymous identity and credit wallet. For team use, share one Apple ID or buy through one managed account so the wallet is shared across devices.
- **Invoicing:** in-app purchase through the App Store; follow Apple's process for a receipt in your region.
- **Retention:** projects are local. There is no cloud backup, so archive finished cuts and scripts periodically.

## Next

- [Download SlideTalk](https://apps.apple.com/us/app/slidetalk-ppt-to-video-ai/id6800015747)
- Choosing a format: [PPTX or PDF](../handbook/pptx-or-pdf.md)
- Caption and export troubleshooting: [subtitles and export](../handbook/subtitles-and-export.md)
- All questions: [FAQ](../faq/README.md)

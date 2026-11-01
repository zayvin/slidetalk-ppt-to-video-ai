# FAQ: PPT to video, AI voiceover, subtitles and pricing

Answers to the questions that come up most often, grouped by topic. Where a number exists, the answer gives the number.

## Getting started

### What is SlideTalk?

SlideTalk is an Apple-native app that turns PowerPoint decks, PDFs and images into narrated videos with AI voiceover, subtitles and scene animations — and generates the cover, title, description, tags and chapters alongside them. One universal app covers macOS, iOS and iPadOS, all available on the App Store.

### How is it different from an ordinary PPT-to-video tool?

Ordinary tools stop at "slides + narration = mp4". SlideTalk does two more things. First, it makes the video sound like a person is teaching: a per-slide AI script, 100+ voices, automatic captions, six scene animations and Ken Burns motion. Second, it makes the video publishable: cover, title, description, tags and chapters generated together. It also runs on an anonymous Apple account — no sign-up, no API keys — and renders on your own machine.

### Can I really make a video in three steps?

Yes. Drop a `.pptx` or `.pdf` into the app; describe the audience and tone in one sentence and pick a narration mode, target platform and voice; review the script slide by slide and generate the voiceover, animations and final cut. The Publish Center produces the cover and title in the same pass. No camera, no editing.

### Who is it for?

If your content already lives on slides, it can become video. The most common users are online course teachers and paid-course authors, Bilibili and YouTube knowledge creators, finance and industry analysts, corporate trainers and product marketers, and Xiaohongshu creators turning posts into video. Role-specific playbooks are in [use cases](../use-cases/README.md).

### I am not a scriptwriter. Can I still use it?

Yes. The AI writes a narration script from each slide and you review it. In practice, rewriting the opening two lines and each slide transition is enough to lift the whole video. If you want better drafts, use the [voiceover writing prompts](../templates/voiceover-prompts.md).

## Files and formats

### Which file formats are supported?

`.pptx`, `.ppsx`, `.pdf`, plus PNG, JPG, HEIC and WEBP images. You can drag files in from Finder, WeChat, Mail or AirDrop.

### PPTX or PDF — which should I use?

PDF renders page by page as a high-resolution image and reproduces the layout exactly, including charts, SmartArt, gradients, unusual fonts and equations — **use PDF when the layout carries meaning**. PPTX rebuilds text, images, shapes and tables at their original coordinates: crisp text and small files, but gradients, charts, SmartArt and native PowerPoint animations are not reproduced — **use PPTX for text-heavy, simple decks**. More detail: [PPTX or PDF](../handbook/pptx-or-pdf.md).

### Do you support old .ppt files or Keynote .key files?

No. `.ppt`, `.pps` and `.key` cannot be parsed directly. Save them as `.pptx` or `.pdf` in PowerPoint or Keynote first.

### How much should go on one slide?

A video is not a handout. Two or three points per slide, body text at 24pt or larger (60pt for vertical video). Information density decides whether anyone watches to the end — far more than any setting in the app.

### What about equations and code?

PDF input is the safest, because equations are preserved as images. With PPTX, equations may become images or drop out, so export those pages as images and add them back. For code, make the screenshot fill at least two-thirds of the slide, or it will be unreadable on a phone.

## Narration and voices

### How many voices are there?

More than a hundred, running on Volcengine Seed-TTS 2.0, grouped into lecturer/education, business/broadcast, warm/lifestyle and trending/character. Speed runs from 0.5x to 2.0x, you can audition line by line, and auditioning costs no credits. Chinese and English are the deepest today, and the library keeps growing.

### What narration modes are available?

Four: solo narration, two-person interview, teacher–student Q&A, and news anchor. Two-person modes automatically give each role a different voice, which suits podcasts, weekly reviews and product teardowns.

### Which languages can the script be in?

Chinese, English, or bilingual. For an overseas edition, brief the AI in the target language rather than translating a finished script — you get prose written in that language instead of translated prose.

### Will the AI voice sound fake?

Three things decide it: sentence length, voice choice and speed. Split long sentences, pick a natural-sounding voice, and sit around 1.05x. Also audition on a single slide before generating ten — do not discover the wrong voice after paying for the whole deck.

### Can I use my own voice?

Not in the current version; voiceover comes from the AI voice library, with no cloning. If "taught by me" is the selling point, record as usual and use the app for captions and covers.

## Picture and subtitles

### Are there subtitles? Can I export .srt?

Yes, and they are automatic. The script is split into CJK-safe short lines and burned into the frame in one of five style presets (including the big short-video style). A sidecar `.srt` ships alongside it for platforms where you want soft subtitles.

### What scene animations are there?

Six: highlight, zoom, spotlight, arrow, underline and bracket. The AI reads what the slide is saying and picks the region worth emphasising, then on-device Vision OCR snaps the box onto the real text lines so it never clips a character in half. You can drag and retime everything in the animation editor.

### Is there camera motion and are there transitions?

Yes. Ken Burns pans and zooms plus cross-fades between slides give static slides room to breathe, so it stops looking like a screen recording. The preview player and the exporter share one compositor, so the preview is the final cut.

### What resolution and length can I export?

480p through 4K, with no length limit. Long decks can take a split point on any page and export as several videos (optionally repeating the last page of the previous segment for continuity), which is what a series or a multi-part upload needs. One-click H.264 re-encoding shrinks the file.

### The export file is too big. What now?

Use the built-in H.264 re-encode. Also note that 4K is several times the size of 1080p, and most platforms cap uploads well below that unless you are re-editing.

## Publishing assets

### Are the cover, title, description and tags really automatic?

Yes. The Publish Center generates a cover per platform (Bilibili 3:2, YouTube 16:9, Shorts 9:16, WeChat Channels 3:4), a batch of title candidates with CTR notes, a 200–500 word description with chapter timestamps and keywords, 5–15 tags per platform, and `chapters.txt` split by script semantics.

### Can it upload straight to Bilibili or YouTube?

Not yet. The current version exports a complete bundle — video, subtitles, cover, title candidates, description, tags and chapters — which you paste into the platform. Direct upload is on the roadmap.

### Can I produce different versions for different platforms?

Yes. Pick the target platform when you create the project and the app adjusts aspect ratio, render size, cover spec and title length limits. Producing a horizontal cut and a vertical cut from the same deck is a common workflow.

## Pricing

### How much does it cost?

The download is free. Importing, editing, auditioning voices, rendering and export are **free forever** (480p to 4K, no length limit, no cap on covers or titles). Only AI generation is metered: narration 1 credit per slide, voiceover 1 credit per 10 characters, AI cover 80 credits per image, title/description/tags 2 credits per run.

### What does a 10-minute video cost in AI credits?

About 352 credits, roughly US$0.50, covering the script and the voiceover. New accounts get 600 credits, enough for about 1.7 ten-slide videos.

### Is it a subscription?

No. Pay per use, credits never expire, no monthly fee and no seat licence.

### What top-up sizes exist?

US$0.99 / US$3.99 / US$9.99 / US$29.99, for 600 / 3,000 / 8,000 / 25,000 credits. The first purchase doubles the credits and removes the export watermark permanently. The App Store shows prices in your local currency.

### Is there a watermark on the export?

Yes until you top up; any first purchase removes it permanently.

### What happens when credits run out?

Every AI run quotes a price and freezes the credits first. If the balance runs out the job pauses, the top-up sheet appears, and the job resumes from the same point after payment — nothing is charged twice.

### Can I get a refund?

Refunds follow Apple's rules, and credits are automatically reversed (the balance can go negative and is offset against your next top-up).

## Account and devices

### Do I need to create an account?

No. The app uses Apple's AppTransaction to establish an anonymous identity and credit wallet, and grants 600 welcome credits on first launch. The developer only ever sees a random account identifier.

### Do credits follow me to another device?

Yes. Every device signed into the same Apple ID shares one wallet across Mac, iPhone and iPad.

### Which OS versions are required?

macOS 15.1+, iOS 17+, iPadOS 17+. It is one universal app across all three.

### Is there a Windows version?

No, and that is the biggest limitation. If you only have Windows machines you will need a Mac or an iPad. A HarmonyOS build is still planned, not shipped.

## Privacy and network

### Is my deck uploaded to a server?

No. Deck copies, slide images, scripts, audio, video and covers live in the app's sandbox container, and rendering runs on-device with AVFoundation. Uninstalling the app deletes the container with it.

### Then what does go over the network?

Only the AI steps: scripts send that slide's text (plus the slide image when visual understanding is on), voiceover sends the text to be read, covers send the title copy and style brief. The gateway does not store your content. Generated audio is cached locally, so repeated lines play instantly.

### Can I work offline?

You can edit an existing project and render without a connection — rendering is entirely local. AI script, voiceover and cover generation need a network.

### How should I handle sensitive material?

Turn off visual understanding (text only, no images), replace sensitive slides with placeholders before importing, or write the script yourself instead of generating it. That advice applies to any tool, not just this one.

## Everything else

### Are there tutorials and templates?

Yes. This repository has [tutorials in 16 languages](../guides/en/README.md), an [editable sample deck with scripts](../examples/chart-lesson/README.md), [storyboards](../templates/storyboard.csv) and a [pre-publish checklist](../templates/export-checklist.md).

### How do I report a problem?

Open an issue on the [GitHub repository](https://github.com/zayvin/slidetalk-ppt-to-video-ai/issues) with the page, the original wording and your suggested change. For app bugs, use "App Support" on the App Store listing.

### Can I use the material commercially?

Yes. The guides, sample deck, scripts, subtitles and worksheets here are CC BY 4.0 — adapt and reuse them commercially with attribution. The SlideTalk app itself is distributed separately through the App Store.

---

Something missing? [Open an issue](https://github.com/zayvin/slidetalk-ppt-to-video-ai/issues), or just [download the app](https://apps.apple.com/us/app/slidetalk-ppt-to-video-ai/id6800015747) — the 600 welcome credits cover about 1.7 ten-slide videos.

# Turn a PowerPoint into a course video without recording yourself

If you teach, the deck is already done. What is missing is the four hours of recording, re-recording and captioning that turn that deck into something a student can watch. This page is the shortest path from a `.pptx` to a publish-ready course video on a Mac, iPhone or iPad — no camera, no microphone, no editing timeline.

## The workflow in one table

| Step | What you do | Time |
| --- | --- | --- |
| 1. Prepare the deck | One idea per slide, body text 24pt or larger | your call |
| 2. Import | Drag the `.pptx` or `.pdf` into SlideTalk | 10 seconds |
| 3. Brief the narrator | One sentence: who is watching and what they should be able to do afterwards | 30 seconds |
| 4. Review the script | Fix the opening two lines and each slide transition | 10–20 minutes |
| 5. Generate | Voiceover, captions, emphasis animations, render | 3–5 minutes |
| 6. Publish | Cover, title, description, tags and chapters are generated too | 5 minutes |

The only steps that need your judgement are 1 and 4. Everything else is mechanical, which is why the same deck that used to take a weekend now takes an evening — and why **fixing one slide costs one slide**, not one re-record.

## Choose the input format on purpose

- **PDF** renders page by page as a high-resolution image. Charts, SmartArt, gradients, unusual fonts and equations survive exactly as designed. Use PDF when the layout carries meaning.
- **PPTX** rebuilds text, images, shapes and tables at their original coordinates. Text stays crisp and files stay small, but gradients, charts, SmartArt and native PowerPoint animations are not reproduced.
- **Images** (PNG, JPG, HEIC, WEBP) work for pages you have already exported or photographed.

Old `.ppt` / `.pps` files and Keynote `.key` files cannot be read directly — save them as `.pptx` or `.pdf` first. More detail: [PPTX or PDF](../../handbook/pptx-or-pdf.md).

## What a course video needs that a demo does not

**Consistency beats novelty.** Pick one voice, one speed and one cover template for the whole series, then stop changing them. Viewers notice a voice change far more than a layout change.

**One idea per slide.** AI narration will faithfully read all eight bullets you put on a slide. Delete six of them. A course is not a handout.

**Chapter-level export.** Put a split point on the first slide of each chapter and export a separate video per chapter. A 40-slide deck becomes five 8-minute lessons that can be sold, reordered or replaced independently.

**A real opening line.** "In this lesson we will look at chapter three" loses the viewer in four seconds. "Your model scores 99% in training and falls apart in production — here is why" keeps them. The AI draft usually opens with the first version; rewrite it.

**Bilingual editions, not translations.** If you sell the same course in English, brief the narrator in English ("explain to US undergraduates why the training accuracy is misleading") rather than translating a Chinese script. The output reads like English, not like translated Chinese.

## Cost of a 10-slide lesson

AI generation for a 10-slide video is roughly 352 credits, about US$0.50–0.60 depending on your App Store region. Importing, editing, auditioning voices, rendering and exporting are free, at any resolution from 480p to 4K and any length. New accounts start with 600 credits, enough for about 1.7 videos. There is no subscription.

## Where it stops

Being clear about limits saves you a wasted afternoon:

- **macOS 15.1+, iOS 17+, iPadOS 17+ only.** No Windows build.
- **No PowerPoint animation import.** Emphasis comes from the six built-in scene animations (highlight, zoom, spotlight, arrow, underline, bracket).
- **Not a video editor.** No music library, no colour grading, no multi-track timeline. If you need a branded intro, render here and finish in your editor.
- **No direct upload.** You get an export bundle; uploading to YouTube or Bilibili is still a manual step.

## Start with something small

The [chart lesson](../../examples/chart-lesson/README.md) is a four-slide deck with an editable PowerPoint, a matching PDF, English and Chinese scripts, and two SRT files. It is designed to be finished in 40 seconds, which makes it a cheap way to test whether a voice and a subtitle style suit your course before you commit a whole term to them.

Ready to try the real thing? [Download SlideTalk](https://apps.apple.com/app/id6800015747) · [Compare the four approaches to PPT-to-video](../../compare/ppt-to-video-tools.md) · [Read the FAQ](../../faq/README.md)

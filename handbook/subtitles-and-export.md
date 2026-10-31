# Add subtitles to a slide video and check the exported MP4

Decide how viewers should see the words before you export. SlideTalk can render captions into the picture and export an SRT subtitle file. These produce different viewing experiences.

| Delivery choice | What the viewer gets | What to test |
| --- | --- | --- |
| Captions burned into the video | Text remains visible in every copy of the picture. | Play the MP4 on its own with the player’s captions switched off. Look for text over labels or controls. |
| A separate SRT track | A compatible player or publishing platform can display or hide the text. | Test with a video that has no visible captions baked into it. Attach the matching SRT and toggle the track during playback. |

If the MP4 already has text in the picture, attaching the SRT as a visible track can put two copies on screen. Switch the player’s captions off and on to identify which layer each copy comes from. Decide which version to publish after testing the actual player.

## Check three places in the finished video

1. **At the start**, check the first spoken word against its cue. An intro inserted after producing the subtitles shifts everything that follows it.
2. **At a slide change**, listen for where the previous sentence ends. If the old caption lingers over a new chart, adjust the cue or move the slide change. Keep a number and its unit together where possible.
3. **Near the end**, check the last complete sentence. If the first cue matches but later cues drift, compare against the final video edit before changing timestamps. A removed pause in the middle requires a different fix than a late start affecting every cue.

## Read one SRT cue

```srt
1
00:00:02,000 --> 00:00:05,000
The revised form took nine minutes.
```

Here the line appears two seconds into the video and clears at five. Each cue has a number, a start and end time, and its text. Leave a blank line before the next cue. When you change the script or re-render the voice, check the timings against the new file.

For a final phone check, watch once without sound and then listen once without looking. On a chart, the viewer should be able to read both the caption and the unit it refers to. For hands-on practice, open the [chart lesson](../examples/chart-lesson/README.md) or the [English quick start](../guides/en/README.md).

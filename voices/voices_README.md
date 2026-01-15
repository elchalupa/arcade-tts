# Voice Reference Files

Place your voice reference files (`.wav` format) in this folder.

## Requirements

- **Duration:** ~10 seconds of clear speech
- **Format:** WAV (16-bit, mono or stereo)
- **Quality:** Minimal background noise
- **Content:** Natural speech (not singing)

## Tips for Good Voice References

1. **Consistent tone** — Keep the same character voice throughout
2. **Clear audio** — Record in a quiet environment
3. **Natural speech** — Read a sentence or two, not single words
4. **Match your intent** — If you want energetic TTS, use an energetic reference

## File Naming

Name your files descriptively:
- `sardonic_bot.wav` — Dry, deadpan delivery
- `yelling_jumpscare.wav` — High energy, loud
- `default_voice.wav` — Your primary voice

## Usage

Update `VOICE_REFERENCE` in `tts_server.py` or set the environment variable:

```bash
export VOICE_REFERENCE=voices/your_voice.wav
```

## ⚠️ Important

Do NOT commit copyrighted voice samples to this repository. Only use:
- Your own voice recordings
- Voices you have permission to use
- Public domain / CC0 licensed samples

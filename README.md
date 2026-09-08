# PORTAL AI MVP

Android prototype for an endless feed of ten-second, AI-generated windows into
imaginary places. Every clip is explicitly labelled as AI-generated.

## Included

- Native Android app in Kotlin/Jetpack Compose
- Full-screen vertical swipe feed
- Video preloading via Android Media3
- 10-second clip limit and automatic advance
- 480p/720p quality metadata
- FastAPI catalogue backend
- Weighted random scene/prompt generator
- Safety rules for synthetic adult characters
- GitHub Actions APK build

## Start the catalogue server

```bash
cd backend
python -m venv .venv
. .venv/bin/activate
pip install -r requirements.txt
uvicorn app.main:app --reload
```

## Add generated videos

Put MP4 files in `backend/media/`, then add their URLs and metadata to the
catalogue. The MVP ships with remote public sample URLs only to test playback;
replace them before publication.

## Business architecture

1. Generate clips asynchronously in batches.
2. Moderate every clip before it enters the public catalogue.
3. Store approved MP4 files in object storage/CDN.
4. Serve a randomized feed with deduplication per user.
5. Generate custom scenes only after payment.

Never market the clips as real live cameras. Use “AI-generated scene” on every
screen and in exported videos.


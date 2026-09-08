import random
import uuid

from fastapi import FastAPI, Query

from .models import Clip, FeedResponse
from .prompt_engine import build_prompt, random_scene

app = FastAPI(title="PORTAL AI Catalogue", version="0.1.0")

# Public samples are playback placeholders, not AI-generated production assets.
SAMPLE_URLS = [
    "https://storage.googleapis.com/gtv-videos-bucket/sample/ForBiggerBlazes.mp4",
    "https://storage.googleapis.com/gtv-videos-bucket/sample/ForBiggerEscapes.mp4",
    "https://storage.googleapis.com/gtv-videos-bucket/sample/ForBiggerFun.mp4",
]


@app.get("/health")
def health() -> dict[str, str]:
    return {"status": "ok"}


@app.get("/v1/feed", response_model=FeedResponse)
def feed(limit: int = Query(default=5, ge=1, le=10)) -> FeedResponse:
    clips = []
    for index in range(limit):
        scene = random_scene()
        clips.append(
            Clip(
                id=str(uuid.uuid4()),
                video_url=SAMPLE_URLS[index % len(SAMPLE_URLS)],
                place=scene.place.title(),
                country=scene.country,
                moment=scene.moment,
                quality=scene.quality,
                prompt=build_prompt(scene),
            )
        )
    random.shuffle(clips)
    return FeedResponse(clips=clips)


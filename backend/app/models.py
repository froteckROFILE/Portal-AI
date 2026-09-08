from pydantic import BaseModel, Field


class Clip(BaseModel):
    id: str
    video_url: str
    place: str
    country: str
    moment: str
    quality: str
    duration_seconds: int = Field(default=10, le=10)
    ai_generated: bool = True
    prompt: str


class FeedResponse(BaseModel):
    clips: list[Clip]
    disclosure: str = "Scènes générées par intelligence artificielle"


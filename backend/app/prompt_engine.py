import random
from dataclasses import dataclass


@dataclass(frozen=True)
class Scene:
    place: str
    country: str
    moment: str
    weather: str
    people: str
    action: str
    quality: str
    camera: str


PLACES = ["public park", "side street", "seaside promenade", "open-air café", "train platform", "forest path"]
COUNTRIES = ["Algeria", "Japan", "Canada", "Brazil", "Italy", "Finland", "South Korea"]
MOMENTS = ["early morning", "late afternoon", "blue hour", "night"]
WEATHER = ["clear", "light rain", "overcast", "windy", "after rainfall"]
PEOPLE = [
    "no person in the foreground",
    "one fictional adult man",
    "one fictional adult woman",
    "two fictional adults",
]
PEOPLE_ACTIONS = ["walking past", "waiting quietly", "jogging in the background", "looking at the scenery", "feeding birds"]
EMPTY_ACTIONS = ["leaves moving in the wind", "distant traffic crossing the frame", "birds briefly landing on the path"]
QUALITIES = ["480p", "540p", "720p"]
CAMERAS = [
    "handheld vertical phone camera with subtle natural shake",
    "vertical rear phone camera with a brief autofocus correction",
    "vertical phone camera with mild compression and imperfect exposure",
]


def random_scene(rng: random.Random | None = None) -> Scene:
    rng = rng or random.SystemRandom()
    people = rng.choice(PEOPLE)
    action = rng.choice(EMPTY_ACTIONS if people == "no person in the foreground" else PEOPLE_ACTIONS)
    return Scene(
        place=rng.choice(PLACES),
        country=rng.choice(COUNTRIES),
        moment=rng.choice(MOMENTS),
        weather=rng.choice(WEATHER),
        people=people,
        action=action,
        quality=rng.choice(QUALITIES),
        camera=rng.choice(CAMERAS),
    )


def build_prompt(scene: Scene) -> str:
    return (
        f"Exactly 10 seconds. {scene.camera}. A believable {scene.place} in "
        f"{scene.country}, {scene.moment}, {scene.weather} weather. {scene.people}; "
        f"{scene.action}. Natural ambient sound, physically plausible motion, "
        f"subtle sensor noise, {scene.quality}. Fictional adults only. No minors, "
        "no celebrity likeness, no readable licence plates, no logos, no violence, "
        "no sexual content, no captions, no camera-facing performance."
    )

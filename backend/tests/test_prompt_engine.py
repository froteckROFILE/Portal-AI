import random

from app.prompt_engine import build_prompt, random_scene


def test_prompt_has_safety_and_format_constraints():
    prompt = build_prompt(random_scene(random.Random(7)))
    assert "Exactly 10 seconds" in prompt
    assert "Fictional adults only" in prompt
    assert any(value in prompt for value in ("480p", "540p", "720p"))


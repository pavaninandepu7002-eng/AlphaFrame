import os
import textwrap
from functools import lru_cache

try:
    import openai
    OPENAI_AVAILABLE = True
except Exception:
    OPENAI_AVAILABLE = False


def _build_prompt(idea: str, mode: str) -> str:
    if mode == 'characters':
        return f"""You are a helpful assistant that creates character profiles.

Idea: {idea}

Provide 3 characters with name, age, short arc, and a brief logline for each."""

    if mode == 'plan':
        return f"""You are a production planner.

Idea: {idea}

Produce a concise production plan including: budget estimate, key crew roles, shooting schedule (high level), and essential locations."""

    # default: screenplay
    return f"""Write a short screenplay scene inspired by the following idea.

Idea: {idea}

Write about 6-12 paragraphs with clear scene headings and dialogue."""


@lru_cache(maxsize=256)
def _cached_generate(idea: str, mode: str, temperature: float, max_tokens: int) -> str:
    prompt = _build_prompt(idea, mode)

    api_key = os.getenv('OPENAI_API_KEY')
    if OPENAI_AVAILABLE and api_key:
        openai.api_key = api_key
        try:
            resp = openai.Completion.create(
                model="text-davinci-003",
                prompt=prompt,
                max_tokens=max_tokens,
                temperature=temperature,
            )
            return resp.choices[0].text.strip()
        except Exception:
            # fall back to simple generator on failure
            pass

    # Fallback simple generator (deterministic and fast)
    if mode == 'characters':
        parts = []
        for i, archetype in enumerate(['Protagonist', 'Antagonist', 'Supporting']):
            # make fallback characters reflect the idea so outputs vary per input
            idea_token = (idea.split()[0].capitalize() if idea else 'Persona')
            name = f"{archetype} {i+1} ({idea_token})"
            # vary ages slightly based on idea length to introduce deterministic variation
            age = 30 + i * 5 + (len(idea) % 7)
            arc = f"Starts as {archetype.lower()} connected to '{idea_token}', ends transformed by conflict related to the idea." 
            logline = f"{name} faces a choice tied to the idea '{idea[:40]}'. This decision defines the story's emotional core."
            parts.append(f"Name: {name}\nAge: {age}\nArc: {arc}\nLogline: {logline}\n")
        return "\n".join(parts)

    if mode == 'plan':
        plan = textwrap.dedent(f"""
        Production Plan for: {idea}

        - Budget (estimate): $50k - $250k (depends on scale)
        - Key Crew: Director, DoP, Producer, Production Designer, Sound Mixer
        - Schedule: 10 shooting days (2-3 locations per day)
        - Locations: 3 primary interiors, 2 exteriors

        Notes: Start with a 2-day prep and 2-day post shoot for editing and sound.
        """)
        return plan

    # screenplay fallback
    scene = textwrap.dedent(f"""
    INT. ROOM - DAY

    A short scene inspired by: {idea}

    A: (quiet) This is the beginning.
    B: (soft) And this is the response.

    They move toward a decision, the stakes quietly rising.

    CUT TO:
    """)
    return scene


def generate(idea: str, mode: str = 'screenplay', temperature: float = 0.8, max_tokens: int = 800) -> str:
    """Public generate wrapper that uses a cached internal generator with model params."""
    temperature = float(temperature)
    max_tokens = int(max_tokens)
    return _cached_generate(idea, mode, temperature, max_tokens)

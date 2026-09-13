"""Defense-in-depth text review; not a comprehensive clinical-advice classifier."""

import re

PATTERNS = (
    r"recommended\s+dose",
    r"increase\s+your\s+dose",
    r"decrease\s+your\s+dose",
    r"take\s+\d+(?:\.\d+)?\s*mg",
    r"stop\s+taking",
    r"best\s+treatment\s+for\s+you",
    r"best\s+medication",
    r"you\s+should\s+take",
)


def check_output(text: str) -> None:
    if any(re.search(pattern, text, re.IGNORECASE) for pattern in PATTERNS):
        raise ValueError("Output requires research guardrail review")

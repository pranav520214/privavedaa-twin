import pytest

from transplant_twin.safety.output_labels import RESEARCH_LABEL
from transplant_twin.safety.research_guardrails import check_output


@pytest.mark.parametrize(
    "text",
    [
        "recommended dose",
        "Increase your dose",
        "decrease your dose",
        "take 2.5 mg",
        "stop taking",
        "best treatment for you",
        "you should take",
    ],
)
def test_blocked_phrases(text):
    with pytest.raises(ValueError):
        check_output(text)


def test_label_passes():
    check_output(RESEARCH_LABEL)

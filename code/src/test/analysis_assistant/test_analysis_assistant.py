import pytest

from src.analysis_assistant.analysis_assistant import Assistant


class TestAssistant:
    def test_is_applicable(self):
        assistant = Assistant()
        is_texts = "Reported problems with telephony, probable source might be an attack on VoIP gate."
        action = {
            "name": "VoIP analysis",
            "regex": "[Vv]oIP",
            "url": "/fmc/voip/"
        }
        assert assistant.is_applicable(action, texts=is_texts)

        not_text = "Lorem ipsum dolor sit amet, consectetuer adipiscing elit."
        assert not assistant.is_applicable(action, texts=not_text)



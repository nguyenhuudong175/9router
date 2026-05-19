from __future__ import annotations

from typing import Any

from .detector import detect_format
from .request_translators import translate_request
from .response_translators import translate_response


class Translator:
    detect_format = staticmethod(detect_format)
    translate_request = staticmethod(translate_request)
    translate_response = staticmethod(translate_response)


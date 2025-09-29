from __future__ import annotations

import re
from dataclasses import dataclass
from typing import List, Optional

from flask import Blueprint, jsonify, render_template, request

from .summarizer import SummarizerService, TranscriptFetchError, ValidationError


bp = Blueprint("routes", __name__)


YOUTUBE_URL_REGEX = re.compile(
    r"^(?:https?://)?(?:www\.)?(?:youtube\.com/watch\?v=|youtu\.be/)([\w-]{11})(?:[&#?].*)?$",
    re.IGNORECASE,
)


@dataclass
class SummarizeRequest:
    url: str
    ratio: float


def parse_request() -> SummarizeRequest:
    data = request.get_json(silent=True) or {}
    url = (data.get("url") or "").strip()
    ratio_raw = data.get("ratio", 0.25)
    try:
        ratio = float(ratio_raw)
    except Exception:
        raise ValidationError("Invalid ratio. Provide a number between 0.05 and 0.8.")
    if not url or not YOUTUBE_URL_REGEX.match(url):
        raise ValidationError("Please provide a valid YouTube URL.")
    if not (0.05 <= ratio <= 0.8):
        raise ValidationError("Ratio must be between 0.05 and 0.8.")
    return SummarizeRequest(url=url, ratio=ratio)


@bp.get("/")
def index():
    return render_template("index.html")


@bp.post("/api/summarize")
def summarize():
    try:
        req = parse_request()
        service = SummarizerService()
        result = service.fetch_and_summarize(req.url, ratio=req.ratio)
        return jsonify({"status": "ok", **result})
    except ValidationError as ve:
        return jsonify({"status": "error", "error": str(ve)}), 400
    except TranscriptFetchError as te:
        return jsonify({"status": "error", "error": str(te)}), 502
    except Exception as e:
        return jsonify({"status": "error", "error": "Unexpected server error."}), 500



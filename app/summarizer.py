from __future__ import annotations

import re
from dataclasses import dataclass
from typing import Dict, List, Optional

from youtube_transcript_api import YouTubeTranscriptApi, TranscriptsDisabled, NoTranscriptFound
from sumy.parsers.plaintext import PlaintextParser
from sumy.nlp.tokenizers import Tokenizer
from sumy.summarizers.text_rank import TextRankSummarizer


class ValidationError(Exception):
    pass


class TranscriptFetchError(Exception):
    pass


YOUTUBE_VIDEO_ID_REGEX = re.compile(r"([\w-]{11})")


def extract_video_id(url: str) -> str:
    match = re.search(r"(?:v=|youtu\.be/)([\w-]{11})", url)
    if not match:
        raise ValidationError("Could not extract video ID from URL.")
    return match.group(1)


def summarize_text(text: str, ratio: float) -> List[str]:
    parser = PlaintextParser.from_string(text, Tokenizer("english"))
    summarizer = TextRankSummarizer()
    # Determine number of sentences by ratio (min 3 sentences)
    total_sentences = len(list(parser.document.sentences))
    count = max(3, int(total_sentences * ratio)) if total_sentences > 0 else 0
    summary_sentences = summarizer(parser.document, count)
    return [str(s) for s in summary_sentences]


@dataclass
class SummarizerService:
    preferred_languages: Optional[List[str]] = None

    def fetch_transcript(self, video_id: str) -> str:
        try:
            transcript_list = YouTubeTranscriptApi.list_transcripts(video_id)
            # Try to find English or user preferred language
            transcript = None
            if self.preferred_languages:
                for lang in self.preferred_languages:
                    try:
                        transcript = transcript_list.find_transcript([lang])
                        break
                    except Exception:
                        continue
            if transcript is None:
                try:
                    transcript = transcript_list.find_transcript(["en"])
                except Exception:
                    # Fallback to any manually created transcript
                    transcript = transcript_list.find_manually_created_transcript([t.language_code for t in transcript_list])

            if transcript is None:
                raise NoTranscriptFound(video_id)

            chunks = transcript.fetch()
            full_text = " ".join(chunk["text"] for chunk in chunks if chunk.get("text"))
            if not full_text.strip():
                raise TranscriptFetchError("Transcript is empty.")
            return full_text
        except TranscriptsDisabled:
            raise TranscriptFetchError("Transcripts are disabled for this video.")
        except NoTranscriptFound:
            raise TranscriptFetchError("No transcript found for this video.")
        except Exception as e:
            raise TranscriptFetchError("Failed to fetch transcript.")

    def fetch_and_summarize(self, url: str, ratio: float = 0.25) -> Dict[str, object]:
        video_id = extract_video_id(url)
        transcript = self.fetch_transcript(video_id)
        summary_sentences = summarize_text(transcript, ratio)
        summary_text = " ".join(summary_sentences)
        return {
            "video_id": video_id,
            "ratio": ratio,
            "summary": summary_text,
            "sentences": summary_sentences,
            "word_count": len(transcript.split()),
            "sentence_count": len(summary_sentences),
        }



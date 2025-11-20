import base64
import json
from typing import List

from google import genai
from fastapi import HTTPException

from app.core.config import settings
from app.schemas.ai_test import HistoryRequest, TutorResponse


class AiTestService:
    def __init__(self):
        self.ai = genai.Client(api_key=settings.AI_KEY)

    async def evaluate(self, file, histories: List[HistoryRequest]) -> TutorResponse:
        try:
            # 파일 bytes → base64
            file_bytes = await file.read()
            base64_data = base64.b64encode(file_bytes).decode("utf-8")
            mime_type = file.content_type or "audio/webm"

            # 프롬프트 생성
            prompt = self.build_prompt(histories)

            # Gemini 호출
            response = self.ai.models.generate_content(
                model="gemini-2.5-flash-lite",
                contents=[
                    {
                        "role": "user",
                        "parts": [
                            {
                                "inlineData": {
                                    "data": base64_data,
                                    "mimeType": mime_type,
                                }
                            },
                            {"text": prompt},
                        ],
                    }
                ],
            )

            # 결과 텍스트 추출
            raw_text = (
                response.candidates[0].content.parts[0].text
                if response.candidates
                else ""
            )

            # 코드펜스 제거
            clean = raw_text.replace("```json", "").replace("```", "").strip()

            # JSON 변환
            return TutorResponse(**json.loads(clean))

        except Exception as e:
            print("AI evaluate error:", e)
            raise HTTPException(
                status_code=500, detail="AI 요청 처리 중 오류가 발생했습니다."
            )

    def build_prompt(self, histories: List[HistoryRequest]) -> str:
        formatted_history = "\n".join(
            [
                f"User ({i + 1}): {entry.user}\nAssistant ({i + 1}): {entry.assistant}"
                for i, entry in enumerate(histories)
            ]
        )

        return f"""
            You are Ken, a friendly English conversation partner.
            You will receive the user's voice input (not text). Listen carefully,
            understand what they said, and respond naturally in English (1–3 sentences).

            After replying, objectively evaluate their spoken English on the following five metrics (0–100):

            {{
                "user": string,            // English transcription of what the user actually said
                "reply": string,           // Natural English reply (1–3 sentences)
                "pronunciation": number,   // 0–100
                "fluency": number,         // 0–100
                "coherence": number        // 0–100
            }}

            Pronunciation Scoring (STRICT):
            - Evaluate strictly based on raw audio.
            - Penalize unclear consonants, missing ending sounds, wrong stress, monotone rhythm, strong Korean-accent patterns.
            - If ANY word is unclear → max 60.
            - If multiple unclear → max 40.
            - 90–100 = near-native clarity only.

            Fluency / Coherence:
            - Fluency: rhythm, hesitation, pauses.
            - Coherence: logical flow of meaning.
            - Be conservative, no inflated scores.

            Global Rules:
            - Strict + objective scoring only.
            - 100 = near-native.
            - 0–20 if heavily distorted or unclear.

            Guidelines:
            - Respond naturally.
            - No teaching, no explanations.
            - Friendly tone only.
            - Keep consistency with past conversation:

            {formatted_history or "(no previous messages)"}

            Respond ONLY in valid JSON.
        """.strip()

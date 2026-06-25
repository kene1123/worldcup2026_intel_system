# GEMINI CONTENT GENERATOR

import time

import google.generativeai as genai

from config import GEMINI_API_KEY


genai.configure(
    api_key=GEMINI_API_KEY
)

model = genai.GenerativeModel(
    "gemini-2.5-flash"
)


def generate_article(
    prompt,
    retries=2
):

    for attempt in range(
        1,
        retries + 1
    ):

        try:
            print("[GEMINI] Calling API...")
            response = model.generate_content(
                prompt
            )

            return response.text

        except Exception as e:

            error_message = str(e)

            print(
                f"[GEMINI ERROR] {error_message}"
            )

            # QUOTA EXHAUSTED DON'T RETRY
            
            if (
                "quota" in error_message.lower()
                or
                "429" in error_message
                or
                "resource_exhausted"
                in error_message.lower()
            ):

                print(
                    "[GEMINI] Daily quota exhausted."
                )

                break

            # TEMPORARY FAILURE RETRY

            if attempt < retries:

                print(
                    f"[GEMINI] Retry "
                    f"{attempt}/{retries}"
                )

                print(
                    "[GEMINI] Waiting 30 seconds..."
                )

                time.sleep(30)

    # FALLBACK CONTENT
    
    return (
        "Article generation failed because "
        "the AI service was unavailable or "
        "the API quota was exceeded. "
        "The World Cup Engine continued "
        "processing successfully."
    )
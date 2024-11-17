import groq
from config import GROQ_API_KEY

groq_client = groq.Client(api_key=GROQ_API_KEY)

def get_llm_results(query, text):
    try:
        if not text:
            return "No relevant text found for GroqAPI processing."
        chat_complete = groq_client.chat.completions.create(
            messages=[
                {
                    "role": "user",
                    "content": f"{query} directly from the text without extra text {text[:500]}"
                }
            ],
            model="mixtral-8x7b-32768",
        )
        return chat_complete.choices[0].message.content if chat_complete.choices else "No response from GroqAPI"
    except Exception as e:
        return f"Error processing with GroqAPI: {e}"

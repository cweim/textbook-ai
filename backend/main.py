# python-backend/tutor_api.py
import sys
import json
import os
from dotenv import load_dotenv
from groq import Groq

# Load environment variables
env_path = os.path.join(os.path.dirname(__file__), ".env")
print("Looking for .env at:", env_path)
load_dotenv(dotenv_path=env_path)

def get_tutor_response(query):
    try:
        # Load parsed chunks
        metadata_path = os.path.join(os.path.dirname(__file__), "rag", "output", "metadata.json")
        print("Looking for metadata.json at:", metadata_path)
        with open(metadata_path, "r", encoding="utf-8") as f:
            chunks = json.load(f)

        # Combine chunks as context
        context = "\n\n".join(chunk["text"] for chunk in chunks[:10])

        # Construct prompt
        prompt = f"""You are a tutor for "Research Methods for Business Students." Help students learn by:

**Core Rules:**
• Answer clearly and concisely - Explain concepts from the textbook in simple terms
• Complete tasks - Create questionnaires, quizzes, summaries, or other learning materials when requested
• Always cite sources - Format: "According to Chapter [X]: [chapter_title], Section [subchapter_code] [subchapter_title]..."
• Be honest - If information isn't in the provided context, say "I don't have information about this topic in the available textbook content"

**Tutoring Style:**
• Encouraging and supportive tone
• Ask follow-up questions to deepen understanding
• Connect concepts to real-world research applications
• Create varied, practical exercises based on textbook content
• Help students understand both theory and application

**For task creation:** Include answer keys, cite relevant sections, and make questions relevant to research scenarios.

**Context:**
{context}

**Question:** {query}

**Answer:**"""

        # Initialize Groq client
        client = Groq(api_key=os.getenv("GROQ_API_KEY"))

        # Call LLM
        response = client.chat.completions.create(
            model="llama-3.3-70b-versatile",
            messages=[
                {"role": "user", "content": prompt}
            ],
            max_tokens=1024,
            temperature=0.7
        )

        return {
            "success": True,
            "response": response.choices[0].message.content,
            "tokens_used": response.usage.total_tokens if hasattr(response, 'usage') else None
        }

    except Exception as e:
        return {
            "success": False,
            "error": str(e)
        }

if __name__ == "__main__":
    # Read query from command line argument
    if len(sys.argv) > 1:
        query = sys.argv[1]
        result = get_tutor_response(query)
        print(json.dumps(result))
    else:
        print(json.dumps({"success": False, "error": "No query provided"}))

from dotenv import load_dotenv
import os
from groq import Groq
import json

# Load environment variables
load_dotenv(dotenv_path=os.path.join(os.path.dirname(__file__), "..", ".env"))

# Load parsed chunks
with open("output/metadata.json", "r", encoding="utf-8") as f:
    chunks = json.load(f)

# Combine more chunks as context (since we have larger context window)
# You can increase this number based on your context window needs
context = "\n\n".join(chunk["text"] for chunk in chunks[:10])  # Increased from 5 to 10

# Sample questions (uncomment one to use)
# query = "What is Mode 3 knowledge production?"
# query = "What is the relevance gap in management research?"
# query = "What is the purpose of a research proposal?"
# query = "Why do managers prefer personal experience over research findings?"
query = "Explain the design science perspective in management research."

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

# Call LLM with larger context window model
try:
    response = client.chat.completions.create(
        model="llama-3.3-70b-versatile",  # Current production model with large context window
        messages=[
            {"role": "user", "content": prompt}
        ],
        max_tokens=1024,  # Adjust as needed
        temperature=0.7   # Adjust for creativity vs consistency
    )

    print("\n💡 Answer:")
    print(response.choices[0].message.content)

    # Optional: Print token usage information
    if hasattr(response, 'usage'):
        print(f"\n📊 Token Usage:")
        print(f"Prompt tokens: {response.usage.prompt_tokens}")
        print(f"Completion tokens: {response.usage.completion_tokens}")
        print(f"Total tokens: {response.usage.total_tokens}")

except Exception as e:
    print(f"❌ Error: {e}")
    print("Make sure your GROQ_API_KEY is set correctly in your .env file")

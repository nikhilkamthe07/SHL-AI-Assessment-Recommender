import os
from dotenv import load_dotenv
from google import genai

# Load environment variables
load_dotenv()

# Configure Gemini client
client = genai.Client(
    api_key=os.getenv("GEMINI_API_KEY")
)


def generate_response(query, assessments):
    """
    Generates a conversational response using Gemini
    based only on the retrieved SHL assessments.
    """

    # Build context from retrieved assessments
    context = ""

    for item in assessments:
        context += f"""
Assessment Name: {item.get('name', '')}
Description: {item.get('description', '')}
URL: {item.get('url', '')}

"""

    prompt = f"""
You are an SHL Assessment Recommendation Assistant.

Your job is to recommend ONLY SHL assessments.

Recruiter Query:
{query}

Retrieved SHL Assessments:
{context}

Rules:

1. If the recruiter query is vague (for example: "I need an assessment"),
   DO NOT recommend assessments immediately.

   Instead politely ask:
   - What role are you hiring for?
   - What is the experience level?
   - Are you looking for technical, cognitive, behavioural or personality assessments?

2. If the user asks anything NOT related to SHL assessments
   (sports, politics, coding help, legal advice, medical advice, etc.),
   politely refuse and say that you only assist with SHL assessment recommendations.

3. Recommend ONLY from the retrieved SHL assessments.

4. Never invent assessment names or URLs.

5. If sufficient information is available,
   recommend between 1 and 10 assessments,
   explain briefly why each assessment fits,
   and include its SHL URL.

6. Keep the answer professional, concise and easy to understand.
"""

    try:

        response = client.models.generate_content(
            model="gemini-2.5-flash",
            contents=prompt,
        )

        return response.text

    except Exception as e:

        return f"Error generating response: {str(e)}"
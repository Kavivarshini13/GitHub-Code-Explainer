import requests


def generate_explanation(code):

    prompt = f"""
You are a code explanation assistant.

Analyze the GitHub repository code given below.

Explain the project in SIMPLE language so that a college student can
understand and present it in a viva.

Use exactly these sections:

## 1. Project Overview
Explain what the project does in 3-5 sentences.

## 2. Technologies Used
List the programming languages, frameworks, libraries, databases,
and important tools found in the code.

## 3. Main Features
List the important features of the project as bullet points.

## 4. How the Project Works
Explain the flow of the project step-by-step.

## 5. Important Files
Mention the important files and explain the purpose of each file.

## 6. Important Programming Concepts
Mention important concepts found in the code, such as:
- Data structures
- Algorithms
- Functions
- Classes
- Database operations
- APIs
- Machine learning or NLP techniques, if present

## 7. Simple Viva Explanation
Give a short explanation that the student can say during a presentation.

IMPORTANT:
- Do not invent features that are not present in the code.
- Base the explanation only on the provided repository code.
- Use simple English.
- Keep the explanation clear and organized.

Repository Code:

{code}
"""

    try:

        response = requests.post(
            "http://localhost:11434/api/generate",
            json={
                "model": "qwen2.5:3b",
                "prompt": prompt,
                "stream": False
            },
            timeout=300
        )

        response.raise_for_status()

        result = response.json()

        return result.get(
            "response",
            "The model did not return an explanation."
        )

    except requests.exceptions.ConnectionError:

        return (
            "Could not connect to the local LLM. "
            "Please make sure Ollama is running."
        )

    except Exception as error:

        return f"Error while generating explanation: {error}"
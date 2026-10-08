from fastapi import FastAPI, HTTPException
from pydantic import BaseModel

from github_processor import (
    clone_repository,
    extract_code,
    prepare_code_for_llm
)

from llm import generate_explanation


app = FastAPI(
    title="GitHub Code Explainer",
    description="Local GenAI application for explaining GitHub repositories"
)


class RepositoryRequest(BaseModel):
    github_url: str


@app.get("/")
def home():

    return {
        "message": "GitHub Code Explainer API is running"
    }


@app.post("/explain")
def explain_repository(
    request: RepositoryRequest
):

    try:

        # ------------------------------------------
        # STEP 1: CLONE REPOSITORY
        # ------------------------------------------

        repo_path = clone_repository(
            request.github_url
        )

        # ------------------------------------------
        # STEP 2: EXTRACT CODE + CONTEXT
        # ------------------------------------------

        code_files, context_files = extract_code(
            repo_path
        )

        # ------------------------------------------
        # CHECK SOURCE CODE
        # ------------------------------------------

        if not code_files:

            raise HTTPException(
                status_code=400,
                detail="No supported source-code files found."
            )

        # ------------------------------------------
        # STEP 3: PREPARE FOR LOCAL LLM
        # ------------------------------------------

        code = prepare_code_for_llm(
            code_files,
            context_files
        )

        # ------------------------------------------
        # STEP 4: GENERATE EXPLANATION
        # ------------------------------------------

        explanation = generate_explanation(
            code
        )

        # ------------------------------------------
        # STEP 5: RETURN RESULT
        # ------------------------------------------

        return {
            "success": True,
            "files_analyzed": len(code_files),
            "context_files": len(context_files),
            "explanation": explanation
        }

    except HTTPException:

        raise

    except Exception as error:

        raise HTTPException(
            status_code=500,
            detail=str(error)
        )
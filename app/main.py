
from fastapi import FastAPI, HTTPException
from bson import ObjectId

from app.database import prompt_collection
from app.schemas import PromptRequest
from app.agent import run_agent

app = FastAPI(
    title="Prompt Storage API",
    description="API to store and retrieve prompts using MongoDB",
    version="1.0.0"
)


@app.get("/")
def home():
    return {
        "message": "Prompt Storage API is running"
    }


@app.post("/prompts")
def create_prompt(data: PromptRequest):

    result = prompt_collection.insert_one(
        {
            "prompt": data.prompt
        }
    )

    return {
        "message": "Prompt stored successfully",
        "id": str(result.inserted_id)
    }


@app.get("/prompts")
def get_prompts():

    prompts = []

    for document in prompt_collection.find():

        prompts.append(
            {
                "id": str(document["_id"]),
                "prompt": document["prompt"]
            }
        )

    return {
        "count": len(prompts),
        "prompts": prompts
    }


@app.get("/prompts/{prompt_id}")
def get_prompt(prompt_id: str):

    try:
        object_id = ObjectId(prompt_id)

    except Exception:
        raise HTTPException(
            status_code=400,
            detail="Invalid prompt ID"
        )

    document = prompt_collection.find_one(
        {
            "_id": object_id
        }
    )

    if document is None:
        raise HTTPException(
            status_code=404,
            detail="Prompt not found"
        )

    return {
        "id": str(document["_id"]),
        "prompt": document["prompt"]
    }

@app.post("/agent")
def agent(prompt: str):

    return run_agent(prompt)

from typing import Any, Dict, List
from app.helpers.prompts import generationPrompt


class GenerationService:

    async def generate(self, question: str, results: List[Dict[str, Any]], model_name: str = "llama3:latest") -> str:
        if results:
            answer = await generationPrompt(question, results, model_name)
        else:
            answer = 'There is not enough information in the uploaded documents to answer the provided question'
        
        return answer

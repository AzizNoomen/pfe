from pydantic import BaseModel, Field
from typing import Any, Dict, Optional, List

from pydantic import BaseModel
from typing import List, Optional

#ollama list models reponse schemas:

class OllamaModelDetails(BaseModel):
    parent_model: str
    format: str
    family: str
    families: List[str]
    parameter_size: str
    quantization_level: str

class OllamaModel(BaseModel):
    name: str
    model: str
    modified_at: str
    size: int
    digest: str
    details: OllamaModelDetails

class OllamaModelListResponse(BaseModel):
    response: List[OllamaModel]


class ShowModelDetails(BaseModel):
    parent_model: str
    format: str
    family: str
    families: List[str]
    parameter_size: str
    quantization_level: str

class ShowModelResponse(BaseModel):
    license: str
    modelfile: str
    parameters: str
    template: str
    details: ShowModelDetails

class ShowModelFullResponse(BaseModel):
    response: ShowModelResponse

class GenericResponse(BaseModel):
    response: Optional[str] = None


class GenerateTextRequest(BaseModel):
    model_name: str
    prompt: str
    system: Optional[str] = None
    template: Optional[str] = None
    context: Optional[List[int]] = None
    options: Optional[Dict[str, Any]] = None


class EncodeRequest(BaseModel):
    prompt: str
    model: str
from pydantic import BaseModel, Field
from typing import Any, Dict, Optional, List

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

class ShowModelResponse(BaseModel):
    license: str
    modelfile: str
    parameters: str
    template: str
    details: OllamaModelDetails

class ShowModelFullResponse(BaseModel):
    response: ShowModelResponse

class GenericResponse(BaseModel):
    response: Optional[str] = None

class GenerateTextRequest(BaseModel):
    model_name: str
    prompt: str
    system: str | None = None
    template: str | None = None
    context: List[int] | None = None
    options: Dict[str, Any] | None = None

class EncodeRequest(BaseModel):
    model_name: str
    prompt: str

class EncodeResponse(BaseModel):
    embedding: List[float]

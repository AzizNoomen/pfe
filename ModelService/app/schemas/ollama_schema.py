from pydantic import BaseModel, Field
from typing import Optional, List

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
    expires_at: str

class OllamaModelListResponse(BaseModel):
    response: List[OllamaModel]


#ollama show model details schemas

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


#ollama generic response

class GenericResponse(BaseModel):
    response: Optional[str] = None

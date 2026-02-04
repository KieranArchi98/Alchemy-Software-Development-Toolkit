from pydantic_settings import BaseSettings
from typing import List, Union, Optional
import json

class Settings(BaseSettings):
    PROJECT_NAME: str = "Alchemy"
    API_V1_STR: str = "/api/v1"
    
    # API Keys
    OPENAI_API_KEY: Optional[str] = None
    
    # CORS
    # Can be a string list like '["http://localhost:5173"]' or a comma separated string
    BACKEND_CORS_ORIGINS: Union[List[str], str] = ["*"]

    class Config:
        case_sensitive = True
        env_file = ".env"

settings = Settings()

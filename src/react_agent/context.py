from pydantic_settings import BaseSettings
from pydantic import Field

class Context(BaseSettings):
    api_key: str = Field(..., env="API_KEY")
    model: str = Field(..., env="MODEL_NAME")

    base_url: str = Field("https://api.openai.com/v1", env="BASE_URL")
    max_search_results: int = Field(5, env="MAX_SEARCH_RESULTS")

    class Config:
        env_file = ".env"

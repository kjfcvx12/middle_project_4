from pydantic import BaseModel

class FavoriteCreate(BaseModel):
    log_id: int
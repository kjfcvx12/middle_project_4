from pydantic import BaseModel, Field

class Favorite_Routine_Base(BaseModel):
    u_id : int
    r_id : int

class Favorite_Routine_Create(Favorite_Routine_Base):
    pass

class Favorite_Routine_In_DB(Favorite_Routine_Base):
    f_r_id : int
    
    
    class Config:
        from_attributes = True

class Favorite_Routine_Read(Favorite_Routine_In_DB):
    pass
from pydantic import BaseModel, Field


class Like_Comment_Base(BaseModel):
    u_id : int
    c_id : int

class Like_Comment_Create(Like_Comment_Base):
    pass

class Like_Comment_In_DB(Like_Comment_Base):
    l_c_id : int

    class Config:
        from_attributes = True

class Like_Comment_Read(Like_Comment_In_DB):
    pass
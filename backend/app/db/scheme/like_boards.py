from pydantic import BaseModel, Field


class Like_Board_Base(BaseModel):
    u_id : int
    b_id : int

class Like_Board_Create(Like_Board_Base):
    pass

class Like_Board_In_DB(Like_Board_Base):
    l_b_id : int

    class Config:
        from_attributes = True

class Like_Board_Read(Like_Board_Base):
    pass
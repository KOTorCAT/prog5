from pydantic import BaseModel

class TermBase(BaseModel):
    term: str
    definition: str

class TermCreate(TermBase):
    pass

class TermUpdate(TermBase):
    pass

class TermResponse(TermBase):
    id: int

    class Config:
        from_attributes = True
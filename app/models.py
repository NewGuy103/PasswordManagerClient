from pydantic import BaseModel


# State models
class AddPasswordEntryData(BaseModel):
    entry_name: str
    username: str
    password: str
    url: str

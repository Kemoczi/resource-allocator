from pydantic import BaseModel

class ResourceCreate(BaseModel):
    location: str
    device: str
    interface_id: str
    phy_speed: str
    optics: str
    assigned: bool

class Resource(BaseModel):
    id: int
    location: str
    device: str
    interface_id: str
    phy_speed: str
    optics: str
    assigned: bool
    class Config:
        # orm_mode = True
        from_attributes = True

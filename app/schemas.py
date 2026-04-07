from pydantic import BaseModel

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


class AssignInterfaceRequest(BaseModel):
    location: str | None = None,
    phy_speed: str | None = None,
    optics: str | None = None
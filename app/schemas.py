from pydantic import BaseModel, ConfigDict

class Resource(BaseModel):
    id: int
    location: str
    device: str
    interface_id: str
    phy_speed: str
    optics: str
    assigned: bool

    model_config = ConfigDict(from_attributes=True)


class AssignInterfaceRequest(BaseModel):
    location: str | None = None
    phy_speed: str | None = None
    optics: str | None = None
from sqlalchemy.orm import Session

from.database import Base, SessionLocal, engine
from.models import Resource


resources = [
    {"location": "London", "device": "PE1", "interface_id": "Port1", "phy_speed": "10G", "optics": "10GBASE-LR", "assigned": False},
    {"location": "London", "device": "PE1", "interface_id": "Port2", "phy_speed": "10G", "optics": "10GBASE-LR", "assigned": False},
    {"location": "London", "device": "PE1", "interface_id": "Port3", "phy_speed": "100G", "optics": "100GBASE-ER", "assigned": False},
    {"location": "London", "device": "PE1", "interface_id": "Port4", "phy_speed": "1G", "optics": "1GBASE-LR", "assigned": False},
    {"location": "London", "device": "PE1", "interface_id": "Port5", "phy_speed": "1G", "optics": "1GBASE-SR", "assigned": False},
    {"location": "London", "device": "PE2", "interface_id": "Port1", "phy_speed": "1G", "optics": "1GBASE-SR", "assigned": False},
    {"location": "London", "device": "PE2", "interface_id": "Port2", "phy_speed": "100G", "optics": "100GBASE-LR", "assigned": False},
    {"location": "London", "device": "PE2", "interface_id": "Port3", "phy_speed": "10G", "optics": "10GBASE-LR", "assigned": False},
    {"location": "London", "device": "PE2", "interface_id": "Port4", "phy_speed": "10G", "optics": "10GBASE-SR", "assigned": False},
    {"location": "London", "device": "PE2", "interface_id": "Port5", "phy_speed": "10G", "optics": "10GBASE-LR", "assigned": False},
]


def init_db() -> None:
    Base.metadata.create_all(bind=engine)

    db: Session = SessionLocal()
    try:
        already_exists = db.query(Resource).first()
        if already_exists:
            return

        db.add_all(Resource(**resource) for resource in resources)
        db.commit()
    finally:
        db.close()


if __name__ == "__main__":
    init_db()

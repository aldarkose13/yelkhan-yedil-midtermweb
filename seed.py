"""Create tables and prefill the DB with 6 criminals and 12 hunt logs.

Run: python seed.py              (wipes and reseeds)
     python seed.py --if-empty   (seeds only if the DB has no criminals)
"""
import sys

from app.database import Base, SessionLocal, engine
from app.models import HuntLog, WantedCriminal

CRIMINALS = [
    dict(name="Jax Orrin", nickname="Void Viper", reward=25000, latitude=34.05, longitude=-118.24,
         last_known_location_note="Last seen near Titan docks", difficulty=8,
         armed=True, has_crew=True, escape_master=True),
    dict(name=None, nickname="Ghost Nebula", reward=50000, latitude=None, longitude=None,
         last_known_location_note="Unknown, rumored in the Kuiper Belt", difficulty=10,
         armed=True, has_crew=False, escape_master=True),
    dict(name="Mara Quill", nickname="Stardust Queen", reward=12000, latitude=51.5, longitude=-0.12,
         last_known_location_note="Mars Station Alpha casino", difficulty=5,
         armed=False, has_crew=True, escape_master=False),
    dict(name="Dex Holloway", nickname="Iron Jaw", reward=4500, latitude=-33.86, longitude=151.2,
         last_known_location_note="Europa mining colony", difficulty=3,
         armed=True, has_crew=False, escape_master=False),
    dict(name="Lin Zhao", nickname="Comet Fox", reward=8000, latitude=35.68, longitude=139.69,
         last_known_location_note="Orbital market, Ceres", difficulty=6,
         armed=False, has_crew=False, escape_master=True),
    dict(name="Borg Vasquez", nickname="Black Hole Bob", reward=75000, latitude=0.0, longitude=0.0,
         last_known_location_note="Edge of Sector 9", difficulty=9,
         armed=True, has_crew=True, escape_master=False),
]

# (criminal index, success, notes)
HUNTS = [
    (0, False, "Target escaped through an asteroid field."),
    (0, False, "Ambushed by his crew near Titan."),
    (0, True, "Captured after a long chase; cargo seized."),
    (1, False, "Lost the signal at the Kuiper Belt."),
    (1, False, "Only found an empty decoy ship."),
    (2, True, "Arrested quietly at the casino."),
    (2, False, "Tip was false, she had left an hour earlier."),
    (3, True, "Easy catch in the mines."),
    (4, False, "Vanished in the market crowd."),
    (4, True, "Cornered at a docking bay."),
    (5, False, "Too heavily guarded; retreated."),
    (5, False, "Shots exchanged, target jumped to hyperspace."),
]

if __name__ == "__main__":
    if "--if-empty" in sys.argv:
        Base.metadata.create_all(bind=engine)
        with SessionLocal() as check:
            if check.query(WantedCriminal).first() is not None:
                print("Database already has data, skipping seed.")
                sys.exit(0)
    else:
        Base.metadata.drop_all(bind=engine)
        Base.metadata.create_all(bind=engine)
    db = SessionLocal()
    criminals = [WantedCriminal(**c) for c in CRIMINALS]
    db.add_all(criminals)
    db.flush()
    db.add_all(
        HuntLog(criminal_id=criminals[i].id, success=s, notes=n) for i, s, n in HUNTS
    )
    db.commit()
    db.close()
    print(f"Seeded {len(CRIMINALS)} criminals and {len(HUNTS)} hunt logs.")

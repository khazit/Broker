from time import sleep
from pathlib import Path
import sqlite3

from broker.core.database import DataBaseManager
from broker.core.models import Job, Event

if __name__ == "__main__":
    empty_db = DataBaseManager("tests/test_data/empty.db")

    db = DataBaseManager("tests/test_data/data.db")
    db.session.add(Job.from_payload({
        "user": "tyler@mail.com",
        "description": "Run a simulation",
        "command": "docker run --gpus all --privileged=true -v /path/to/somewhere/or/something/:/work -v /home/path/to/some/data/set/data/:/data --name train --rm tensorflow python run_experiments.py experiments/experiment.json",
    }))
    job1 = db.session.query(Job).filter_by(identifier=1).first()
    sleep(1)
    job1.events.append(Event(status=2))
    sleep(1)
    job1.events.append(Event(status=3))
    sleep(1)
    job1.events.append(Event(status=5))

    db.session.add(Job.from_payload({
        "user": "boy@mail.com",
        "description": "Compute something important",
        "command": "echo 'I speak giberish'",
    }))
    job2 = db.session.query(Job).filter_by(identifier=2).first()
    job2.events.append(Event(status=2))
    sleep(1)
    job2.events.append(Event(status=3))
    sleep(1)
    job2.events.append(Event(status=4))

    db.session.add(Job.from_payload({
        "user": "scott@mail.com",
        "description": "Run OCR",
        "command": "df -h",
    }))
    job3 = db.session.query(Job).filter_by(identifier=3).first()
    job3.events.append(Event(status=2))
    sleep(1)
    job3.events.append(Event(status=3))

    db.session.add(Job.from_payload({
        "user": "jim@mail.com",
        "description": "Train an AGI",
        "command": "echo 'He done'",
    }))
    job4 = db.session.query(Job).filter_by(identifier=4).first()
    job4.events.append(Event(status=2))

    db.session.add(Job.from_payload({
        "user": "creator@mail.com",
        "description": "Run a 100 years job",
        "command": "docker ps",
    }))
    job5 = db.session.query(Job).filter_by(identifier=5).first()
    job5.events.append(Event(status=2))

    db.session.add(Job.from_payload({
        "user": "good@mail.com",
        "description": "Test a script",
        "command": "sleep 15",
    }))
    job6 = db.session.query(Job).filter_by(identifier=6).first()
    job6.events.append(Event(status=2))
    db.session.commit()

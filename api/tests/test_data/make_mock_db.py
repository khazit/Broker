from pathlib import Path

import sqlite3

from broker.core.database import DataBaseManager
from broker.core.utils import Job

if __name__ == "__main__":
    empty_db = DataBaseManager("tests/test_data/empty.db")

    db = DataBaseManager("tests/test_data/data.db")
    db.session.add(Job.from_payload({
        "user": "tyler@mail.com",
        "description": "run an experiment",
        "command": "docker run --gpus all --privileged=true -v /path/to/somewhere/or/something/:/work -v /home/path/to/some/data/set/data/:/data --name train --rm tensorflow python run_experiments.py experiments/experiment.json",
    }))
    job1 = db.session.query(Job).filter_by(identifier=1).first()
    job1.status = 5
    db.session.add(Job.from_payload({
        "user": "boy@mail.com",
        "description": "Cant speak",
        "command": "echo 'I speak giberish'",
    }))
    job2 = db.session.query(Job).filter_by(identifier=2).first()
    job2.status = 4
    db.session.add(Job.from_payload({
        "user": "scott@mail.com",
        "description": "No space",
        "command": "df -h",
    }))
    job3 = db.session.query(Job).filter_by(identifier=3).first()
    job3.status = 3
    db.session.add(Job.from_payload({
        "user": "jim@mail.com",
        "description": "G O O D",
        "command": "echo 'He done'",
    }))
    db.session.add(Job.from_payload({
        "user": "creator@mail.com",
        "description": "Check on my dockers",
        "command": "docker ps",
    }))
    db.session.add(Job.from_payload({
        "user": "good@mail.com",
        "description": "Nap time",
        "command": "sleep 15",
    }))
    db.session.commit()

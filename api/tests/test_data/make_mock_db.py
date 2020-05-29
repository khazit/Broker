import sqlite3


if __name__ == "__main__":
    conn = sqlite3.connect("tests/test_data/data.db", check_same_thread=False)
    cursor = conn.cursor()
    cursor.execute(
        "CREATE TABLE jobs ("
        "identifier INT PRIMARY KEY,"
        "user VARCHAR(50),"
        "status INT,"
        "description MEDIUMTEXT,"
        "command MEDIUMTEXT"
        ")"
    )
    cursor.execute(
        "INSERT INTO jobs VALUES ("
        "'0',"
        "'tyler@mail.com',"
        "'2',"
        "'run an experiment',"
        "'docker run --gpus all --privileged=true -v /path/to/somewhere/or/something/:/work -v /home/path/to/some/data/set/data/:/data --name train --rm tensorflow python run_experiments.py experiments/experiment.json'"
        ")"
    )
    cursor.execute(
        "INSERT INTO jobs VALUES ("
        "'3',"
        "'boy@mail.com',"
        "'0',"
        "'Cant speak',"
        "'echo \"I speak giberish\"'"
        ")"
    )
    cursor.execute(
        "INSERT INTO jobs VALUES ("
        "'4',"
        "'scott@mail.com',"
        "'4',"
        "'No space',"
        "'df -h'"
        ")"
    )
    cursor.execute(
        "INSERT INTO jobs VALUES ("
        "'5',"
        "'jim@mail.com',"
        "'5',"
        "'G O O D',"
        "'echo \"He done\"'"
        ")"
    )
    cursor.execute(
        "INSERT INTO jobs VALUES ("
        "'7',"
        "'creator@mail.com',"
        "'2',"
        "'Check on my dockers',"
        "'docker ps'"
        ")"
    )
    cursor.execute(
        "INSERT INTO jobs VALUES ("
        "'8',"
        "'good@mail.com',"
        "'2',"
        "'Nap time',"
        "'sleep 15'"
        ")"
    )
    conn.commit()

    conn = sqlite3.connect("tests/test_data/empty.db", check_same_thread=False)
    cursor = conn.cursor()
    cursor.execute(
        "CREATE TABLE jobs ("
        "identifier INT PRIMARY KEY,"
        "user VARCHAR(50),"
        "status INT,"
        "description MEDIUMTEXT,"
        "command MEDIUMTEXT"
        ")"
    )

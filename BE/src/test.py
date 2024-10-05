import sqlite3
import bcrypt

if __name__ == "__main__":
    print(
        bcrypt.hashpw(
            "!Duong2001".encode("utf-8"),
            bcrypt.gensalt(),
        ).decode("utf-8")
    )

    # conn01 = sqlite3.connect("data/db.sqlite3")
    # conn02 = sqlite3.connect("data/db.sqlite3")
    # conn01.close()
    # conn02.commit()
    # conn02.close()

import sqlite3 as sql
import sqlite3

DB_PATH = "database/data_source.db"


def listCommunities():
    con = sql.connect(DB_PATH)
    cur = con.cursor()
    data = cur.execute("SELECT * FROM Communities").fetchall()
    con.close()
    return data


def listPosts():
    con = sql.connect(DB_PATH)
    cur = con.cursor()
    data = cur.execute(
        """
        SELECT p.PostID, p.Title, p.Content, u.Username, c.CommunityName, p.Image
        FROM Posts p
        JOIN Users u ON p.UserID = u.UserID
        JOIN Communities c ON p.CommunityID = c.CommunityID
        ORDER BY p.CreatedAt DESC
        """
    ).fetchall()
    con.close()

    posts = [
        {
            "id": row[0],
            "title": row[1],
            "content": row[2],
            "author": row[3],
            "community": row[4],
            "image": row[5] if len(row) > 5 else None,
        }
        for row in data
    ]
    return posts


def listUsers():
    con = sql.connect(DB_PATH)
    cur = con.cursor()
    data = cur.execute("SELECT * FROM Users").fetchall()
    con.close()
    return data


def getUserByUsername(username):
    con = sql.connect(DB_PATH)
    cur = con.cursor()
    row = cur.execute("SELECT * FROM Users WHERE Username = ?", (username,)).fetchone()
    con.close()
    if row:
        return {
            "UserID": row[0],
            "Username": row[1],
            "Password": row[2],
            "Bio": row[3],
            "YearGroup": row[4],
            "AcademicAchievements": row[5],
        }
    return None


def login(username, password):
    user = getUserByUsername(username)
    if user and user["Password"] == password:
        return True, user
    return False, None


def add_friend(user_id, friend_id):
    con = sql.connect("database/data_source.db")
    cur = con.cursor()
    cur.execute(
        "INSERT INTO Friends (UserID, FriendID) VALUES (?, ?)", (user_id, friend_id)
    )
    con.commit()
    con.close()


def get_friends(user_id):
    con = sql.connect("database/data_source.db")
    cur = con.cursor()
    data = cur.execute(
        """
        SELECT u.UserID, u.Username
        FROM Friends f
        JOIN Users u ON f.FriendID = u.UserID
        WHERE f.UserID = ?
        """,
        (user_id,),
    ).fetchall()
    con.close()
    return [{"id": row[0], "username": row[1]} for row in data]


def get_db_connection():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn


def validate_user(username, password):
    conn = get_db_connection()
    user = conn.execute(
        "SELECT * FROM users WHERE username = ? AND password = ?", (username, password)
    ).fetchone()
    conn.close()
    return user


def get_all_communities():
    conn = get_db_connection()
    communities = conn.execute("SELECT * FROM communities").fetchall()
    conn.close()
    return communities

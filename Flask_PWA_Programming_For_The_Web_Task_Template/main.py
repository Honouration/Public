from flask import Flask, render_template, request, redirect, url_for, session, flash
import sqlite3

app = Flask(__name__)
app.secret_key = "supersecretkey"


def get_db_connection():
    conn = sqlite3.connect("database/data_source.db")
    conn.row_factory = sqlite3.Row
    return conn


@app.route("/", methods=["GET"])
@app.route("/index.html", methods=["GET"])
def index():
    conn = get_db_connection()
    posts = conn.execute("SELECT * FROM Posts").fetchall()
    conn.close()
    return render_template("index.html", posts=posts)


@app.route("/communities", methods=["GET"])
def communities():
    conn = get_db_connection()
    communities_list = conn.execute("SELECT * FROM Communities").fetchall()
    conn.close()
    return render_template("communities.html", communities=communities_list)


@app.route("/community/<int:community_id>")
def community(community_id):
    conn = get_db_connection()
    community_item = conn.execute(
        "SELECT * FROM Communities WHERE CommunityID = ?", (community_id,)
    ).fetchone()
    conn.close()

    if community_item:
        return render_template("community.html", community=community_item)
    else:
        return "Community not found", 404


@app.route("/post/<int:post_id>")
def post(post_id):
    conn = get_db_connection()
    post_item = conn.execute(
        "SELECT * FROM Posts WHERE PostID = ?", (post_id,)
    ).fetchone()
    conn.close()

    if post_item:
        return render_template("post.html", post=post_item)
    else:
        return "Post not found", 404


@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]

        conn = get_db_connection()
        user = conn.execute(
            "SELECT * FROM Users WHERE Username=? AND Password=?",
            (username, password),
        ).fetchone()
        conn.close()

        if user:
            session["user_id"] = user["UserID"]
            session["username"] = user["Username"]
            flash("Login successful!", "success")
            return redirect(url_for("index"))
        else:
            flash("Invalid username or password.", "danger")

    return render_template("login.html")


@app.route("/logout")
def logout():
    session.clear()
    flash("You have been logged out.", "success")
    return redirect(url_for("index"))


@app.route("/friends", methods=["GET"])
def friends():
    if "user_id" not in session:
        flash("You must be logged in to view friends.", "warning")
        return redirect(url_for("login"))

    conn = get_db_connection()
    friends_list = conn.execute(
        """
        SELECT U.Username
        FROM Friends F
        JOIN Users U ON F.FriendUserID = U.UserID
        WHERE F.UserID = ?
        """,
        (session["user_id"],),
    ).fetchall()
    conn.close()

    return render_template("friends.html", friends=friends_list)


@app.route("/add_friend", methods=["POST"])
def add_friend():
    if "user_id" not in session:
        flash("You must be logged in to add friends.", "warning")
        return redirect(url_for("login"))

    friend_username = request.form["friend_username"]

    conn = get_db_connection()
    friend = conn.execute(
        "SELECT UserID FROM Users WHERE Username = ?", (friend_username,)
    ).fetchone()

    if friend:
        existing = conn.execute(
            "SELECT * FROM Friends WHERE UserID=? AND FriendUserID=?",
            (session["user_id"], friend["UserID"]),
        ).fetchone()

        if not existing:
            conn.execute(
                "INSERT INTO Friends (UserID, FriendUserID) VALUES (?, ?)",
                (session["user_id"], friend["UserID"]),
            )
            conn.commit()
            flash(f"{friend_username} has been added to your friends list!", "success")
        else:
            flash(f"{friend_username} is already your friend.", "warning")
    else:
        flash("User not found.", "danger")

    conn.close()
    return redirect(url_for("friends"))


if __name__ == "__main__":
    app.run(debug=True)

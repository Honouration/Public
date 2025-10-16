--CREATE TABLE extension(
  extID INTEGER NOT NULL PRIMARY KEY,
  name TEXT NOT NULL,
  hyperlink TEXT NOT NULL,
  about TEXT NOT NULL,
  image TEXT NOT NULL,
  language TEXT NOT NULL

--CREATE TABLE Users (
    UserID INTEGER PRIMARY KEY,
    Username TEXT NOT NULL,
    Password TEXT NOT NULL,
    Bio TEXT,
    YearGroup TEXT,
    AcademicAchievements TEXT
);


--CREATE TABLE Communities (
    CommunityID INTEGER PRIMARY KEY,
    CommunityName TEXT NOT NULL
);


--CREATE TABLE Posts (
    PostID INTEGER PRIMARY KEY,
    UserID INTEGER,
    Title TEXT NOT NULL,
    Content TEXT NOT NULL,
    CommunityID INTEGER,
    CreatedAt DATE,
    FOREIGN KEY(UserID) REFERENCES Users(UserID),
    FOREIGN KEY(CommunityID) REFERENCES Communities(CommunityID)
);


--CREATE TABLE Friends (
    FriendID INTEGER PRIMARY KEY,
    UserID INTEGER,
    FriendUserID INTEGER,
    FOREIGN KEY(UserID) REFERENCES Users(UserID),
    FOREIGN KEY(FriendUserID) REFERENCES Users(UserID)
);

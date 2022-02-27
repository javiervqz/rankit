# Rankit
Find the rankpage of all url's within a website to visualize connections. Strenght of connection is based on [page rank algorithm](https://en.wikipedia.org/wiki/PageRank)



# About

## Error Codes in db Pages
- 100: links fetched, html fine
- 120: links not fetch, html fine 
- 150: html null for some reaseon, seems to be an html/txt

## DataBase Schema
```SQL
CREATE TABLE Pages(
id INTEGER PRIMARY KEY,
url TEXT UNIQUE,
html TEXT,
error INTEGER,
old_rank REAL,
new_rank REAL,
id_website INTEGER
);

CREATE TABLE Websites(
id INTEGER PRIMARY KEY,
url TEXT UNIQUE
);

CREATE TABLE Links(
from_id INTEGER,
to_id INTEGER
);
```

# Mini Search Engine
Find the rankpage of all url's within a website to get most relevant result using pagerank algorithm.

## Motivation
Besides learing about web crawling and the algorithm that created the internet as we know it, the idea is to find the relevancy for every professor in fing.uach. This can help you find a professor to help you with Thesis, projects or any question in [Fing_crawler][FCurl]


[FCurl]: <https://github.com/javiervqz/Fing_crawler>

## Error Codes in db Pages
 100: links fetched, html fine
 120: links not fetch, html fine 
 150: html null for some reaseon, seems to be an html/txt

## DataBase Schema
REATE TABLE Pages(
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


#!/bin/bash
# Bash script to reset tinygen to defaults when testing
whiptail --yesno "This will reset your Tinygen instance to defaults, deleting all pages, posts, & config! This script mainly meant for development purposes!" 20 50

if [[ $? != 0 ]]
then
  echo "Not reseting!"
  exit 0
fi

echo "Deleted rss feed"
rm generated/blog/feed.rss
rm generated/*.html
rm generated/*.css
rm generated/images/*
rm generated/blog/images/*
echo "Cleaned site index, css, and images"
rm generated/blog/*.html
rm generated/blog/*.css
echo "Cleaned generated/blog"
rm source/posts/*.html
echo "Cleaned source/posts"
rm source/pages/*.html
echo "Cleaned source/pages"
rm source/posts/drafts/*.html
echo "Cleaned drafts"
sqlite3 .data/posts.db "drop table posts;"
sqlite3 .data/posts.db "CREATE TABLE posts(ID INTEGER PRIMARY KEY AUTOINCREMENT, title text not null, date text);"
echo "Reset posts database"
rm config.cfg
echo "Deleted config.cfg"
exit 0

#!/usr/bin/env bash
set -e
if [ -z "$1" ]; then
  echo "Usage: ./git_push.sh https://github.com/your-username/ExpoEye.git"
  exit 1
fi
REPO=$1
git init
git add .
git commit -m "chore: expoeye+ groq integrated submission"
git branch -M main
git remote add origin $REPO
git push -u origin main
echo "Pushed to $REPO"

#!/usr/bin/env bash
set -e

# 1) Ensure remote is set
echo "Adding or updating GitHub remote..."
git remote add origin https://github.com/alanoj/OrangeForge.git 2>/dev/null || git remote set-url origin https://github.com/alanoj/OrangeForge.git

# 2) Ensure branch is main
CURRENT=$(git rev-parse --abbrev-ref HEAD)
if [ "$CURRENT" != "main" ]; then
  echo "Renaming current branch ($CURRENT) to main..."
  git branch -M main
else
  echo "Already on main branch"
fi

# 3) Commit changes (if any)
echo "Staging all changes..."
git add .

if git diff --cached --quiet; then
  echo "No changes to commit"
else
  echo "Committing changes..."
  git commit -m "Initial commit — OrangeForge terminal configs"
fi

# 4) Push to GitHub
echo "Pushing to GitHub..."
git push -u origin main

echo "🎉 Done! Repo is now pushed to https://github.com/alanoj/OrangeForge"
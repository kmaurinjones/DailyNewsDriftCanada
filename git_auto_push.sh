#!/bin/sh

# Check for a commit message argument
if [ "$#" -eq 0 ]; then
    COMMIT_MSG="Auto-commit: Update changes"
else
    COMMIT_MSG="$1"
fi

# Add all changes to the staging area
git add .

# Commit the changes
git commit -m "$COMMIT_MSG"

# Push the changes
git push
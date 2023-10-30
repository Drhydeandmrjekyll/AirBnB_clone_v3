#!/bin/bash

# Configuration
MAIN_BRANCH="master"
FEATURE_BRANCH="storage_get_count"
REMOTE_NAME="origin"

# Ensure you are on the main branch
current_branch=$(git symbolic-ref --short HEAD)
if [ "$current_branch" != "$MAIN_BRANCH" ]; then
    echo "Error: You must be on the main branch to perform this operation."
    exit 1
fi

# Fetch the latest changes from the remote repository
git fetch "$REMOTE_NAME"

# Check if the feature branch exists remotely
if git rev-parse --verify "$REMOTE_NAME/$FEATURE_BRANCH" > /dev/null 2>&1; then
    # Ensure there are no uncommitted changes
    if [ -n "$(git status -s)" ]; then
        echo "Error: You have uncommitted changes. Please commit or stash them before merging."
        exit 1
    fi

    # Prompt for confirmation before merging
    read -p "Merge $FEATURE_BRANCH into $MAIN_BRANCH? (y/n): " confirm
    if [ "$confirm" != "y" ]; then
        echo "Merge aborted."
        exit 0
    fi

    # Merge the feature branch into the main branch
    git merge "$REMOTE_NAME/$FEATURE_BRANCH" --no-ff

    # Check if the merge was successful
    if [ $? -eq 0 ]; then
        echo "Merge successful."

        # Push the changes to the remote repository
        git push "$REMOTE_NAME" "$MAIN_BRANCH"
        echo "Changes pushed to remote repository."

        # Optionally, you can delete the feature branch both locally and remotely
        git branch -d "$FEATURE_BRANCH"
        git push "$REMOTE_NAME" --delete "$FEATURE_BRANCH"
        echo "Feature branch deleted."

    else
        echo "Error: Merge failed. Resolve conflicts and commit the changes manually."
        exit 1
    fi

else
    echo "Error: The feature branch '$FEATURE_BRANCH' does not exist remotely."
    exit 1
fi


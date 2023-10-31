#!/bin/bash

# Function to back up local changes
backup_local_changes() {
    local branch_name=$(git rev-parse --abbrev-ref HEAD)
    local backup_dir="branch_backups"

    # Create a backup directory if it doesn't exist
    mkdir -p "$backup_dir"

    # Check if there are local changes
    if [[ $(git status --porcelain) ]]; then
        echo "Backing up local changes for branch '$branch_name'..."
        local timestamp=$(date +"%Y%m%d%H%M%S")
        local backup_file="$backup_dir/${branch_name}_backup_$timestamp.tar.gz"
        git stash save "Backup local changes - $timestamp"
        git stash show -p -u | tar -czf "$backup_file" -T -
        echo "Local changes backed up to '$backup_file'."
    else
        echo "No local changes to back up for branch '$branch_name'."
    fi
}

# Function to override the local branch with the remote branch
override_local_with_remote() {
    local branch_name=$(git rev-parse --abbrev-ref HEAD)

    echo "Fetching the latest changes from the remote repository..."
    git fetch

    echo "Resetting the local branch '$branch_name' to match the remote branch..."
    git reset --hard "origin/$branch_name"

    echo "Local branch '$branch_name' has been overridden with the remote branch."
}

# Main script execution
backup_local_changes
override_local_with_remote

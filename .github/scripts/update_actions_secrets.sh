#!/bin/bash

# Default secrets
DG_READTHEDOCS_ID=${READTHEDOCS_ID}

# Helper functions
function get_secrets_url_notification() {
    REPO_URL="https://github.com/$1"
    [ "x$1" == "x" ] && REPO_URL=$(git config --get remote.origin.url | sed 's/:\/\/[^@]*@/:\/\//' | sed 's/\.git$//')
    echo "You can check project secrets at $REPO_URL/settings/secrets/actions"
}

# Check GitHub CLI availability
[ "x$(which gh)" == "x" ] && echo "Run $(tput bold)sudo apt install gh$(tput sgr0) to install GitHub CLI" && exit -1
gh auth status || echo "$(get_secrets_url_notification)" && exit -1 # Use `gh auth login` if fail

# Set up secrets on repo level
REPO_NAME=$(gh repo view --json owner,name -q '.owner.login + "/" + .name')
gh secret set DG_READTHEDOCS_ID -r $REPO_NAME <<< "$DG_READTHEDOCS_ID"

# Inform about success and further steps
echo "$(get_secrets_url_notification)"
echo "Run $(tput bold)gh auth logout$(tput sgr0) if finished"

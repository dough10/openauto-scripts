#!/bin/bash

ENV_FILE=~/.openauto-scripts/.env

if [[ -f "$ENV_FILE" ]]; then
  echo "$(date '+%Y-%m-%d %H:%M:%S') - .env file found, sourcing variables..."
  source "$ENV_FILE"
else
  echo "$(date '+%Y-%m-%d %H:%M:%S') - .env file not found, using default values..."
fi

LOC=${REC_LOC:-"$HOME/Videos"}

if [[ -d "$LOC" ]]; then
  echo "$(date '+%Y-%m-%d %H:%M:%S') - Removing .h264 files older than 2 weeks from: $LOC"
  find "$LOC" -name "*.h264" -mtime +14 -exec rm -v {} \;
else
  echo "$(date '+%Y-%m-%d %H:%M:%S') - Directory $LOC does not exist."
fi

echo "$(date '+%Y-%m-%d %H:%M:%S') - complete"

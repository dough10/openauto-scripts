#!/bin/bash

ENV_FILE=~/.openauto-scripts/.env

if [[ -f "$ENV_FILE" ]]; then
  echo ".env file found, sourcing variables..."
  # shellcheck disable=SC1090
  source "$ENV_FILE"
else
  echo ".env file not found, using default values..."
fi

LOC=${REC_LOC:-"$HOME/Videos"}

if [[ -d "$LOC" ]]; then
  echo "removing recording from: $LOC"
  # rm -v "$LOC"/*.h264
else
  echo "Directory $LOC does not exist."
fi
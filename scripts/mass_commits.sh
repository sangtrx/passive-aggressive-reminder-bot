#!/bin/bash
set -euo pipefail

# Create 100 small commits by appending a line to MASS_COMMITS.md.
# Each commit's author/committer date is set 60s apart starting from now.

FILE="MASS_COMMITS.md"
START_TS=$(date +%s)

for i in $(seq 1 100); do
  TS=$((START_TS + i * 60))
  # macOS/BSD date: use -r to convert seconds-since-epoch
  DATE_ISO=$(date -u -r "$TS" +"%Y-%m-%dT%H:%M:%SZ")
  echo "Commit $i at $DATE_ISO" >> "$FILE"
  GIT_AUTHOR_DATE="$DATE_ISO" GIT_COMMITTER_DATE="$DATE_ISO" git add "$FILE" \
    && GIT_AUTHOR_DATE="$DATE_ISO" GIT_COMMITTER_DATE="$DATE_ISO" git commit -m "chore(mass): commit $i at $DATE_ISO"
done

echo "Done: created 100 commits (file: $FILE)"

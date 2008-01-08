#!/bin/bash

SOURCE="$1"
TARGET="$2"
TITLE=`grep "$TARGET" files.txt | while IFS=: read fname indent title; do echo "$title"; done`

if [ -z "$SOURCE" -o -z "$TARGET" -o -z "$TITLE" ]; then
	echo "Usage: $0 source target"
	exit 1
fi

cat part0 > "$TARGET"

echo -en "    <title>$TITLE</title>\n" >> "$TARGET"

cat part1 >> "$TARGET"

cat links.txt >> "$TARGET"

cat part2 >> "$TARGET"

cat "$SOURCE" >> "$TARGET"

cat part3 >> "$TARGET"

exit 0

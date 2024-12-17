#!/bin/bash
echo "Enter Verse: "
read user_input
echo "$user_input" | python3 GetRelated.py | ./index.sh $(fzf -m --preview="batcat --color=always {}")

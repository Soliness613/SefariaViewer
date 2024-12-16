#!/bin/bash
echo "Enter Verse: "
read user_input
echo "$user_input" | python3 Ref.py | fx

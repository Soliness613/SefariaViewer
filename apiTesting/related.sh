#!/bin/bash
echo "Enter Verse: "
read user_input
echo "$user_input" | python3 Related.py | fx

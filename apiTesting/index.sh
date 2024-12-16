#!/bin/bash
echo "Enter Index: "
read user_input
echo "$user_input" | python3 Index.py | fx

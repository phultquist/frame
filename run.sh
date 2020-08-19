#!/bin/bash
until pinrt.py; do
    echo "'print.py' crashed with exit code $?. Restarting..." >&2
    sleep 1
done
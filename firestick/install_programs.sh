#!/bin/bash

for file in *.apk; do
    echo Installing $file
    adb install -r $file
done

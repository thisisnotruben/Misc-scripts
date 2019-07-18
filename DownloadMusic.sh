#!/bin/bash

for URL in "$@"
do
youtube-dl --extract-audio --audio-format mp3 --audio-quality 0 $URL
done

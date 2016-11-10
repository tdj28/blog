#!/bin/bash
cd DockerPelican/blog
/usr/bin/python /usr/local/bin/pelican content -s publishconf.py
rsync -avr output/* ../../
cd ../../

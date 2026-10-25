@echo off
cd /d "..\png_output"

rem create movie with 2 frame
ffmpeg -framerate 1 -i frame%%04d.png -vf "scale=ceil(iw/2)*2:ceil(ih/2)*2" -c:v libx264 -pix_fmt yuv420p output.mp4
pause

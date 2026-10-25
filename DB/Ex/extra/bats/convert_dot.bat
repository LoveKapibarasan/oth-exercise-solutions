@echo off
mkdir "..\png_output"

REM generate png files
for %%f in ("..\output\*.dot") do (
   dot -Tpng -Gdpi=1000 "%%f" -o "..\png_output\%%~nf.png"
)
pause

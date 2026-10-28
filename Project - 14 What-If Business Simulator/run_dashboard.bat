@echo off
TITLE Mahindra & Mahindra - What-If Business Simulator Dashboard (Port 5014)
echo ==============================================================================
echo  PROJECT - 14: WHAT-IF BUSINESS SIMULATOR
echo  Mahindra & Mahindra Ltd. — Automotive Cross-Functional Decision Intelligence
echo ==============================================================================

set PYTHON_CMD=python
where python >nul 2>nul
if %errorlevel% neq 0 (
    set PYTHON_CMD="C:\Users\hp\AppData\Local\Programs\Orange\python.exe"
)

echo Starting Executive Decision Intelligence Server on Port 5014...
%PYTHON_CMD% run_project.py
pause


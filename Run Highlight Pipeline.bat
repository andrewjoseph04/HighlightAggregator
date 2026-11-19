@echo off
setlocal

REM Run the Google Sheets to Obsidian end-to-end highlight pipeline.
set "PROJECT_DIR=R:\Coding\HighlightAggregator"

if not exist "%PROJECT_DIR%\Scripts\run_pipeline.py" (
    echo ERROR: Could not find the pipeline at:
    echo   %PROJECT_DIR%\Scripts\run_pipeline.py
    echo Update PROJECT_DIR in this file if the repository is in a different location.
    echo.
    pause
    exit /b 1
)

cd /d "%PROJECT_DIR%"
echo Starting Highlight Aggregator pipeline...
echo Project: %PROJECT_DIR%
echo.

where py >nul 2>nul
if %errorlevel%==0 (
    py -3 Scripts\run_pipeline.py
) else (
    where python >nul 2>nul
    if %errorlevel%==0 (
        python Scripts\run_pipeline.py
    ) else (
        echo ERROR: Python was not found. Install Python 3 and try again.
        echo.
        pause
        exit /b 1
    )
)

set "PIPELINE_EXIT_CODE=%errorlevel%"
echo.
if "%PIPELINE_EXIT_CODE%"=="0" (
    echo Pipeline finished successfully.
) else (
    echo Pipeline failed with exit code %PIPELINE_EXIT_CODE%.
)
pause
exit /b %PIPELINE_EXIT_CODE%

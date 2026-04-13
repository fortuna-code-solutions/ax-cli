@echo off
echo === fortuna-bot setup ===
echo.

python --version 2>nul
if errorlevel 1 (
    echo ERROR: Python not found. Install Python 3.10+ from python.org
    pause
    exit /b 1
)

echo Installing dependencies...
pip install typer httpx rich tomli >nul 2>&1
echo Done.

if exist ".ax\config.toml" (
    echo.
    echo Config found: .ax\config.toml
    echo.
    echo Run the demo:
    echo   run_demo.bat
    echo.
) else (
    echo.
    echo No config found. You need:
    echo   1. A PAT from https://next.paxai.app - Settings - Credentials
    echo   2. Your space ID (from ax spaces list)
    echo.
    echo Create .ax\config.toml with:
    echo   base_url = "https://next.paxai.app"
    echo   token = "axp_a_your_token_here"
    echo   space_id = "your-space-id"
    echo   agent_name = "fortuna-bot"
    echo   agent_id = "your-agent-id"
    echo.
)
pause

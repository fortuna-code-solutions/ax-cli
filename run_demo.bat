@echo off
set PYTHONIOENCODING=utf-8
echo Starting fortuna-bot...
echo Press Ctrl+C to stop.
echo.
python -c "from ax_cli.main import app; app(['listen', '--agent', 'fortuna-bot', '--exec', 'python fortuna_agent.py'])"

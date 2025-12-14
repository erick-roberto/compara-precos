@echo off
echo Iniciando projeto ComparaPrecos...

REM ====== INICIAR BACKEND ======
echo Iniciando Backend...
start cmd /k "cd backend && venv\Scripts\activate && python app.py"

REM ====== INICIAR FRONTEND ======
echo Iniciando Frontend...
start cmd /k "cd frontend && npm run dev"

echo Tudo iniciado!

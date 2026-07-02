#!/usr/bin/env bash
# ============================================================
#  Ascendrite Platform Manager
#  Manages backend (FastAPI :8000) and frontend (Vite :5173)
# ============================================================

DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
BACKEND_PORT=8000
FRONTEND_PORT=5173

# ── OS detection ─────────────────────────────────────────────
is_windows() {
  [[ "$OSTYPE" == "msys" || "$OSTYPE" == "cygwin" ]]
}

# ── Port helpers ─────────────────────────────────────────────

# is_port_listening <port>  →  returns 0 (true) if port is in use
is_port_listening() {
  local port="$1"
  if is_windows; then
    netstat -ano 2>/dev/null | grep -q "LISTENING.*:${port} "
  else
    lsof -i TCP:"${port}" -sTCP:LISTEN -t >/dev/null 2>&1
  fi
}

# kill_port <port>  →  kills every PID listening on <port>
kill_port() {
  local port="$1"
  if is_windows; then
    local pids
    pids=$(netstat -ano 2>/dev/null | grep "LISTENING" | grep ":${port} " | awk '{print $5}' | sort -u)
    for pid in $pids; do
      taskkill //f //pid "$pid" >/dev/null 2>&1 || kill -9 "$pid" >/dev/null 2>&1
    done
  else
    local pids
    pids=$(lsof -t -i TCP:"${port}" -sTCP:LISTEN 2>/dev/null)
    for pid in $pids; do
      kill -9 "$pid" >/dev/null 2>&1
    done
  fi
}

# wait_for_port <port> <max_seconds>  →  returns 0 when port is up, 1 on timeout
wait_for_port() {
  local port="$1" max="$2" i=0
  while (( i < max )); do
    if is_port_listening "$port"; then return 0; fi
    sleep 1; (( i++ ))
  done
  return 1
}

# ── Service actions ──────────────────────────────────────────

start_backend() {
  if is_port_listening "$BACKEND_PORT"; then
    echo ""
    echo "  [INFO]  Backend is already running on http://127.0.0.1:${BACKEND_PORT}"
    sleep 2; return
  fi
  echo ""
  echo "  Starting backend..."
  cd "$DIR/server"
  if is_windows; then
    nohup python-venv-3.10.11/Scripts/python.exe -m uvicorn main:app \
      --host 127.0.0.1 --port "$BACKEND_PORT" >> backend.log 2>&1 </dev/null &
  else
    nohup ./python-venv-3.10.11/bin/python -m uvicorn main:app \
      --host 127.0.0.1 --port "$BACKEND_PORT" >> backend.log 2>&1 </dev/null &
  fi
  if wait_for_port "$BACKEND_PORT" 10; then
    echo "  [OK]  Backend is ON  --  http://127.0.0.1:${BACKEND_PORT}"
  else
    echo "  [WARN]  Backend may still be starting. Check server/backend.log"
  fi
  sleep 2
}

stop_backend() {
  if ! is_port_listening "$BACKEND_PORT"; then
    echo ""
    echo "  [INFO]  Backend is already stopped."
    sleep 2; return
  fi
  echo ""
  echo "  Stopping backend..."
  kill_port "$BACKEND_PORT"
  echo "  [OK]  Backend is OFF."
  sleep 2
}

start_frontend() {
  if is_port_listening "$FRONTEND_PORT"; then
    echo ""
    echo "  [INFO]  Frontend is already running on http://localhost:${FRONTEND_PORT}"
    sleep 2; return
  fi
  echo ""
  echo "  Starting frontend..."
  cd "$DIR/client"
  nohup npm run dev >> frontend.log 2>&1 </dev/null &
  if wait_for_port "$FRONTEND_PORT" 15; then
    echo "  [OK]  Frontend is ON  --  http://localhost:${FRONTEND_PORT}"
  else
    echo "  [WARN]  Frontend may still be starting. Check client/frontend.log"
  fi
  sleep 2
}

stop_frontend() {
  if ! is_port_listening "$FRONTEND_PORT"; then
    echo ""
    echo "  [INFO]  Frontend is already stopped."
    sleep 2; return
  fi
  echo ""
  echo "  Stopping frontend..."
  kill_port "$FRONTEND_PORT"
  echo "  [OK]  Frontend is OFF."
  sleep 2
}

# ── Main loop ────────────────────────────────────────────────

while true; do
  clear
  echo ""
  echo "  ================================================================"
  echo "          Ascendrite Platform Manager"
  echo "  ================================================================"
  echo ""

  if is_port_listening "$BACKEND_PORT"; then
    echo "    [RUNNING]  Backend   |  http://127.0.0.1:${BACKEND_PORT}"
  else
    echo "    [STOPPED]  Backend   |  port ${BACKEND_PORT}"
  fi

  if is_port_listening "$FRONTEND_PORT"; then
    echo "    [RUNNING]  Frontend  |  http://localhost:${FRONTEND_PORT}"
  else
    echo "    [STOPPED]  Frontend  |  port ${FRONTEND_PORT}"
  fi

  echo ""
  echo "  ================================================================"
  echo "    1.  Turn on  Backend"
  echo "    2.  Turn on  Frontend"
  echo "    3.  Turn off Backend"
  echo "    4.  Turn off Frontend"
  echo "    5.  Turn off Both & Exit"
  echo "  ================================================================"
  echo ""

  read -rp "  Choice (1-5): " choice
  echo ""

  case "$choice" in
    1) start_backend   ;;
    2) start_frontend  ;;
    3) stop_backend    ;;
    4) stop_frontend   ;;
    5)
      echo "  Shutting everything down..."
      if is_port_listening "$BACKEND_PORT"; then
        kill_port "$BACKEND_PORT"
        echo "  - Backend stopped."
      else
        echo "  - Backend was already stopped."
      fi
      if is_port_listening "$FRONTEND_PORT"; then
        kill_port "$FRONTEND_PORT"
        echo "  - Frontend stopped."
      else
        echo "  - Frontend was already stopped."
      fi
      echo ""
      echo "  Goodbye."
      sleep 2
      exit 0
      ;;
    *)
      echo "  [ERROR]  Invalid choice. Please enter 1-5."
      sleep 2
      ;;
  esac
done

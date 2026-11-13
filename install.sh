#!/usr/bin/env sh
set -eu

OMNESIGHT_HOME="${OMNESIGHT_HOME:-$HOME/.omnesight}"
VENV_DIR="$OMNESIGHT_HOME/venv"
BIN_DIR="${OMNESIGHT_BIN_DIR:-$HOME/.local/bin}"
INSTALL_SOURCE="${OMNESIGHT_INSTALL_SOURCE:-omnesight}"
GITHUB_SOURCE="git+https://github.com/Omnesight/omnesight-python.git"

echo "Installing Omnesight CLI & Python SDK into $VENV_DIR..."

if command -v python3 >/dev/null 2>&1; then
  PYTHON_BIN="python3"
elif command -v python >/dev/null 2>&1; then
  PYTHON_BIN="python"
else
  echo "Error: python3 is required to install Omnesight CLI." >&2
  exit 1
fi

mkdir -p "$OMNESIGHT_HOME" "$BIN_DIR"
"$PYTHON_BIN" -m venv "$VENV_DIR"

if [ "$INSTALL_SOURCE" = "omnesight" ]; then
  if ! "$VENV_DIR/bin/pip" install --upgrade pip >/dev/null 2>&1; then
    true
  fi
  if ! "$VENV_DIR/bin/pip" install --upgrade "$INSTALL_SOURCE"; then
    echo "PyPI package not reachable yet, falling back to GitHub source..."
    "$VENV_DIR/bin/pip" install --upgrade "$GITHUB_SOURCE"
  fi
else
  "$VENV_DIR/bin/pip" install --upgrade "$INSTALL_SOURCE"
fi

ln -sf "$VENV_DIR/bin/omnesight" "$BIN_DIR/omnesight"
"$BIN_DIR/omnesight" --version

case ":$PATH:" in
  *":$BIN_DIR:"*) ;;
  *)
    echo "Add $BIN_DIR to your PATH to invoke 'omnesight' anywhere:"
    echo "  export PATH=\"$BIN_DIR:\$PATH\""
    ;;
esac

echo "Done! Launch the interactive shell with: omnesight shell"


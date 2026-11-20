#!/bin/bash
set -e
DIR="$(cd "$(dirname "$0")" && pwd)"
APP="$DIR/fakeupdate.py"
DESKTOP="$HOME/Desktop"
SHORTCUT="$DESKTOP/FakeUpdate.command"

if ! command -v python3 >/dev/null 2>&1; then
  echo "Python 3 fehlt. Bitte installiere Python 3 und starte dieses Skript erneut."
  read -r -p "Enter zum Beenden..."
  exit 1
fi

cat > "$SHORTCUT" <<EOF
#!/bin/bash
cd "$DIR"
python3 "$APP"
EOF
chmod +x "$SHORTCUT"
chmod +x "$APP"
echo "Desktop-Verknüpfung erstellt: $SHORTCUT"
open "$SHORTCUT"

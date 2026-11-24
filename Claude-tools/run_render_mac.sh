#!/bin/bash
# Mac-native render (needed for YafaRay: its native libraries ship inside the Sweet Home 3D app).
# Usage: ENGINE=yafaray|sunflow [JOPT="-Dt=<epoch ms>"] ./run_render_mac.sh file.sh3d cams.txt outdir W H LOW|HIGH [views]
# Needs a Java launcher: brew install openjdk
cd "$(dirname "$0")"
APP="/Applications/Sweet Home 3D.app/Contents/app"
JAVA="${JAVA:-/opt/homebrew/opt/openjdk/bin/java}"
CP="$(ls "$APP"/*.jar | tr '\n' ':')"
exec "$JAVA" -Xmx6g ${JOPT} -Dengine="${ENGINE:-yafaray}" -Djava.library.path="$APP" -Dj3d.rend=noop -Dapple.awt.UIElement=true \
  --add-exports java.desktop/com.apple.eio=ALL-UNNAMED --add-exports java.desktop/com.apple.eawt=ALL-UNNAMED --add-exports java.desktop/sun.awt=ALL-UNNAMED --add-exports java.desktop/sun.awt.image=ALL-UNNAMED --add-opens java.desktop/sun.awt=ALL-UNNAMED --add-opens java.desktop/sun.awt.image=ALL-UNNAMED --add-opens java.base/java.lang=ALL-UNNAMED -cp "$CP" S15Tool.java render "$@"

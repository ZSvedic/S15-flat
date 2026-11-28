#!/bin/zsh
# One command per model version: export, lights, inputs, incremental links, Blender in the background.
# Usage (from the repo root): Claude-tools/blender/render_version.sh <prev tag> <new tag> [samples=128] [--full|--keep-day]
#   --keep-day: the change is lights only, so the day renders of vPREV are linked (no day re-render)
#   e.g. Claude-tools/blender/render_version.sh v21 v22 64
# Then, when render/blender/out/run-<new tag>.log ends with "S15 done":
#   <venv>/bin/python Claude-tools/blender/mix.py render/blender/out Renders/blender-lighting "Hrnetička lighting – <new tag>" <new tag>
#   python3 Claude-tools/make_site.py <new tag>
set -e
P=$1; N=$2; SMP=${3:-128}; FULL=$4
R=$(cd "$(dirname $0)/../.." && pwd); T=$R/Claude-tools; IN=$R/render/blender/in; OUT=$R/render/blender/out
J=(/opt/homebrew/opt/openjdk/bin/java --add-exports java.desktop/com.apple.eio=ALL-UNNAMED -Duser.home=$IN/.jhome -Djava.io.tmpdir=$IN/.jhome -Djava.awt.headless=true -Dj3d.rend=noop -cp "$(ls $T/jars/*.jar | tr '\n' ':')")
mkdir -p $IN/.jhome $IN/obj${N#v} $OUT
cd $T && $J ExportObj.java $R/Hrneticka-$N.sh3d $IN/obj${N#v}/s15.obj
unzip -p $R/Hrneticka-$N.sh3d Home.xml > $IN/Home-$N.xml
python3 $T/blender/make_lights.py $IN/Home-$N.xml $IN/lights.json | tail -1
cp $T/blender/groups.json $T/blender/s15_blender.py $T/cams.txt $IN/
python3 $T/blender/rerender.py $R/Hrneticka-$P.sh3d $R/Hrneticka-$N.sh3d $P $N $OUT $FULL
cd $IN
if [[ -n $FG ]]; then                                   # FG=1: wait for Blender (for chained runs)
  S15_TAG=$N caffeinate -i /Applications/Blender.app/Contents/MacOS/Blender -b -P s15_blender.py -- . obj${N#v} ../out 1440 1080 $SMP > $OUT/run-$N.log 2>&1
  echo "Blender done; log: render/blender/out/run-$N.log"
else
  S15_TAG=$N nohup caffeinate -i /Applications/Blender.app/Contents/MacOS/Blender -b -P s15_blender.py -- . obj${N#v} ../out 1440 1080 $SMP > $OUT/run-$N.log 2>&1 &
  echo "Blender started; log: render/blender/out/run-$N.log"
fi

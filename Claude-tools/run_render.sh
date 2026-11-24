#!/bin/bash
cd "$(dirname "$0")"
xvfb-run -a -s "-screen 0 1280x1024x24" java -Xmx2500m ${JOPT} -Dj3d.rend=noop -cp "jars/Examples.jar:jars/Furniture.jar:jars/Help.jar:jars/SweetHome3D.jar:jars/Textures.jar:jars/batik-svgpathparser-1.7.jar:jars/freehep-vectorgraphics-svg-2.1.1c.jar:jars/gluegen-rt.jar:jars/j3dcore.jar:jars/j3dutils.jar:jars/jeksparser-calculator.jar:jars/jmf.jar:jars/jnlp.jar:jars/jogl-java3d.jar:jars/sunflow-0.07.3i.jar:jars/vecmath.jar:" S15Tool.java render "$@"

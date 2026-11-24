import com.eteks.sweethome3d.io.DefaultUserPreferences;
import com.eteks.sweethome3d.io.HomeFileRecorder;
import com.eteks.sweethome3d.j3d.PhotoRenderer;
import com.eteks.sweethome3d.model.*;
import com.eteks.sweethome3d.swing.PlanComponent;

import javax.imageio.ImageIO;
import java.awt.*;
import java.awt.image.BufferedImage;
import java.io.*;
import java.nio.file.*;
import java.util.*;
import java.util.List;

/** Headless helper: check / plan (SVG+PNG) / render (SunFlow) for a .sh3d file. */
public class S15Tool {
  public static void main(String[] a) throws Exception {
    if (!a[0].equals("render")) System.setProperty("java.awt.headless", "true");
    String mode = a[0];
    Home home = new HomeFileRecorder(0, false, null, false, true).readHome(a[1]);
    int walls = home.getWalls().size(), rooms = home.getRooms().size();
    int pieces = 0, doors = 0;
    for (HomePieceOfFurniture p : allPieces(home.getFurniture())) { pieces++; if (p instanceof HomeDoorOrWindow) doors++; }
    System.out.println("loaded: walls=" + walls + " rooms=" + rooms + " pieces=" + pieces + " doorsWindows=" + doors
        + " wallHeight=" + home.getWallHeight());
    if (mode.equals("check")) return;

    if (mode.equals("plan")) {
      UserPreferences prefs = new DefaultUserPreferences();
      prefs.setUnit(LengthUnit.CENTIMETER);
      PlanComponent plan = new PlanComponent(home, prefs, null);
      plan.setBackground(Color.WHITE);
      try (OutputStream out = new BufferedOutputStream(new FileOutputStream(a[2]))) { plan.exportToSVG(out); }
      float scale = Float.parseFloat(a[4]);
      plan.setScale(scale);
      Dimension d = plan.getPreferredSize();
      plan.setSize(d);
      BufferedImage img = new BufferedImage(d.width, d.height, BufferedImage.TYPE_INT_RGB);
      Graphics2D g = img.createGraphics();
      g.setColor(Color.WHITE); g.fillRect(0, 0, d.width, d.height);
      g.setRenderingHint(RenderingHints.KEY_ANTIALIASING, RenderingHints.VALUE_ANTIALIAS_ON);
      plan.paint(g);
      g.dispose();
      ImageIO.write(img, "png", new File(a[3]));
      System.out.println("plan written " + d);
      return;
    }

    if (mode.equals("render")) {
      // a[2] cameras file: name x y z yawDeg pitchDeg fovDeg ; a[3] outdir ; a[4] w ; a[5] h ; a[6] LOW|HIGH ; a[7] optional name filter
      List<String> lines = Files.readAllLines(Paths.get(a[2]));
      int w = Integer.parseInt(a[4]), h = Integer.parseInt(a[5]);
      com.eteks.sweethome3d.j3d.AbstractPhotoRenderer.Quality q = com.eteks.sweethome3d.j3d.AbstractPhotoRenderer.Quality.valueOf(a[6]);
      // -Dengine=yafaray needs SH3D's native libraries: -Djava.library.path=<Sweet Home 3D app folder> (Mac/Windows/x64 Linux)
      String engine = System.getProperty("engine", "sunflow").equals("yafaray")
          ? "com.eteks.sweethome3d.j3d.YafarayRenderer" : "com.eteks.sweethome3d.j3d.PhotoRenderer";
      String only = a.length > 7 ? a[7] : null;
      Compass c = home.getCompass();
      home.setCamera(home.getObserverCamera()); // ceilings are only built in virtual-visit mode
      for (String l : lines) {
        l = l.trim();
        if (l.isEmpty() || l.startsWith("#")) continue;
        String[] t = l.split("\\s+");
        if (only != null && !Arrays.asList(only.split(",")).contains(t[0])) continue;
        Camera cam = new Camera(Float.parseFloat(t[1]), Float.parseFloat(t[2]), Float.parseFloat(t[3]),
            (float) Math.toRadians(Float.parseFloat(t[4])), (float) Math.toRadians(Float.parseFloat(t[5])),
            (float) Math.toRadians(Float.parseFloat(t[6])));
        Camera ref = home.getCamera();
        cam.setTime(Long.getLong("t", 1792584000000L)); // 2026-10-21 14:00 Zagreb
        cam.setLens(ref.getLens());
        long t0 = System.currentTimeMillis();
        com.eteks.sweethome3d.j3d.AbstractPhotoRenderer r = com.eteks.sweethome3d.j3d.AbstractPhotoRenderer.createInstance(engine, home, null, q);
        BufferedImage img = new BufferedImage(w, h, BufferedImage.TYPE_INT_ARGB);
        r.render(img, cam, null);
        r.dispose();
        BufferedImage rgb = new BufferedImage(w, h, BufferedImage.TYPE_INT_RGB);
        Graphics2D g = rgb.createGraphics(); g.drawImage(img, 0, 0, null); g.dispose();
        ImageIO.write(rgb, "png", new File(a[3], t[0] + ".png"));
        System.out.println("rendered " + t[0] + " in " + (System.currentTimeMillis() - t0) / 1000 + " s");
      }
    }
  }

  static List<HomePieceOfFurniture> allPieces(List<HomePieceOfFurniture> l) {
    List<HomePieceOfFurniture> r = new ArrayList<>();
    for (HomePieceOfFurniture p : l) {
      if (p instanceof HomeFurnitureGroup) r.addAll(allPieces(((HomeFurnitureGroup) p).getFurniture()));
      else r.add(p);
    }
    return r;
  }
}

import com.eteks.sweethome3d.io.HomeFileRecorder;
import com.eteks.sweethome3d.model.*;
import com.eteks.sweethome3d.j3d.Object3DBranchFactory;
import java.lang.reflect.Method;

/** Headless OBJ export of a .sh3d (same code path as 3D view > Export to OBJ format). Usage: ExportObj in.sh3d out.obj */
public class ExportObj {
  public static void main(String[] a) throws Exception {
    Home home = new HomeFileRecorder(0, false, null, false, true).readHome(a[0]);
    home.setCamera(home.getObserverCamera());           // virtual-visit mode: ceilings are exported
    Class<?> c = Class.forName("com.eteks.sweethome3d.swing.HomePane$OBJExporter");
    Method m = c.getDeclaredMethod("exportHomeToFile", Home.class, String.class, String.class, boolean.class,
        com.eteks.sweethome3d.viewcontroller.Object3DFactory.class);
    m.setAccessible(true);
    long t0 = System.currentTimeMillis();
    m.invoke(null, home, a[1], "S15 export", true, new Object3DBranchFactory());
    System.out.println("exported in " + (System.currentTimeMillis() - t0) / 1000 + " s");
  }
}

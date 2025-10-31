import maya.cmds as cmds
import random

def do_random(
    use_selection=True,
    do_color=False,
    do_scale=False,
    do_rotation=False,
    do_position=False
):
    if not use_selection:
        print("Apply to Selected is OFF")
        return

    # Use a short variable name
    sel = cmds.ls(selection=True, long=True) 
    if not sel:
        cmds.warning("Select an object first!")
        return

    print(f"Randomizing items: {sel}")

    for obj in sel:
        
        print(f"--- Now working on: {obj} ---")

        if do_color:
            try:
                shader_name = f"random_{obj.replace('|', '_')}_lamSweet"
                shader = cmds.shadingNode('lambert', asShader=True, name=shader_name)
                
                sg_name = f"{shader_name}_SG"
                sg = cmds.sets(renderable=True, noSurfaceShader=True, empty=True, name=sg_name)
                
                cmds.connectAttr(f"{shader}.outColor", f"{sg}.surfaceShader", force=True)
                
                r = random.random()
                g = random.random()
                b = random.random()
                cmds.setAttr(f"{shader}.color", r, g, b, type="double3")

                cmds.sets(obj, edit=True, forceElement=sg)
                
                print(f"Created shader {shader_name} for {obj}")
                
            except Exception as e:
                cmds.warning(f"Failed to set color for {obj}: {e}")
        if do_scale:
            try:
                sx = random.uniform(0.5, 2.0)
                sy = random.uniform(0.5, 2.0)
                sz = random.uniform(0.5, 2.0)
                cmds.setAttr(f"{obj}.scale", sx, sy, sz, type="double3")
            except Exception as e:
                cmds.warning(f"Failed to set Scale for {obj}: {e}")
        if do_rotation:
            try:
                rx = random.uniform(0, 360)
                ry = random.uniform(0, 360)
                rz = random.uniform(0, 360)
                cmds.setAttr(f"{obj}.rotate", rx, ry, rz, type="double3")
            except Exception as e:
                cmds.warning(f"Failed to set Rotate for {obj}: {e}")
        if do_position:
            try:
                px = random.uniform(-10, 10)
                py = random.uniform(-10, 10)
                pz = random.uniform(-10, 10)
                
                cmds.move(px, py, pz, obj, absolute=True, worldSpace=True)
            except Exception as e:
                cmds.warning(f"Failed to move {obj}: {e}")
            
    print("Randomize DONE!!")
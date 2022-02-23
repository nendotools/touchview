
input_mode_items = [('ORBIT','rotate','Rotate the viewport'),
                    ('PAN','pan','Move the viewport'),
                    ('DOLLY','zoom','Zoom in/out the viewport')]

position_items   = [('TOP','top','Set Gizmo position to top of viewport'),
                    ('RIGHT','right','Set Gizmo position to right of viewport'),
                    ('BOTTOM','bottom','Set Gizmo position to bottom of viewport'),
                    ('LEFT','left','Set Gizmo position to left of viewport')]

pivot_items      = [("SURFACE", "Surface", "Sets the pivot position to the surface under the cursor."),
                    ("ACTIVE", "Active Vertex", "Sets the pivot position to the active vertex position."),
                    ("UNMASKED", "Unmasked", "Sets the pivot position to the average position of the unmasked vertices."),
                    ("ORIGIN", "Origin", "Sets the pivot to the origin of the sculpt."),
                    ("BORDER", "Mask Border", "Sets the pivot position to the center of the border of the mask.")]

pivot_icon_items = [("BORDER","PIVOT_BOUNDBOX"),
                    ("ORIGIN","PIVOT_CURSOR"),
                    ("UNMASKED","CLIPUV_HLT"),
                    ("ACTIVE","PIVOT_ACTIVE"),
                    ("SURFACE","PIVOT_MEDIAN")]

edit_modes       = [("OBJECT","Object Mode",""),
                    ("EDIT_MESH","Edit Mode",""),
                    ("SCULPT","Sculpt Mode",""),
                    ("PAINT_VERTEX","Vertex Paint Mode",""),
                    ("PAINT_WEIGHT","Weight Paint Mode",""),
                    ("PAINT_TEXTURE","Texture Paint Mode","")]


input_mode_items = [('ORBIT','rotate','Rotate the viewport'),
                    ('PAN','pan','Move the viewport'),
                    ('DOLLY','zoom','Zoom in/out the viewport')]

position_items   = [('TOP','top','Set Gizmo position to top of viewport'),
                    ('RIGHT','right','Set Gizmo position to right of viewport'),
                    ('BOTTOM','bottom','Set Gizmo position to bottom of viewport'),
                    ('LEFT','left','Set Gizmo position to left of viewport')]

pivot_items      = [("ORIGIN", "Origin", "Sets the pivot to the origin of the sculpt."),
                    ("UNMASKED", "Unmasked", "Sets the pivot position to the average position of the unmasked vertices."),
                    ("BORDER", "Mask Border", "Sets the pivot position to the center of the border of the mask."),
                    ("ACTIVE", "Active Vertex", "Sets the pivot position to the active vertex position."),
                    ("SURFACE", "Surface", "Sets the pivot position to the surface under the cursor.")]

pivot_icon_items = [("BORDER","PIVOT_BOUNDBOX"),
                    ("ORIGIN","PIVOT_CURSOR"),
                    ("UNMASKED","PIVOT_INDIVIDUAL"),
                    ("ACTIVE","PIVOT_MEDIAN"),
                    ("SURFACE","PIVOT_ACTIVE")]

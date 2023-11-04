# type: ignore
from bpy.props import (BoolProperty, CollectionProperty, EnumProperty,
                       FloatProperty, FloatVectorProperty, IntProperty,
                       StringProperty)
from bpy.types import AddonPreferences, Context, PropertyGroup

from .lib.constants import (double_click_items, edit_modes, gizmo_sets,
                            menu_defaults, menu_orientation_items,
                            menu_style_items, pivot_items, position_items)


##
# Action Menu Settings
##
class MenuModeGroup(PropertyGroup):
    mode: StringProperty(name='mode', default='OBJECT')
    menu_slot_1: StringProperty(name='Menu Item', default='')
    menu_slot_2: StringProperty(name='Menu Item', default='')
    menu_slot_3: StringProperty(name='Menu Item', default='')
    menu_slot_4: StringProperty(name='Menu Item', default='')
    menu_slot_5: StringProperty(name='Menu Item', default='')
    menu_slot_6: StringProperty(name='Menu Item', default='')
    menu_slot_7: StringProperty(name='Menu Item', default='')
    menu_slot_8: StringProperty(name='Menu Item', default='')


class OverlaySettings(AddonPreferences):
    bl_idname = __package__

##
# Viewport Control Options
##
    is_enabled: BoolProperty(name='Enable Controls', default=True)
    lazy_mode: BoolProperty(
        name='Lazy Mode',
        default=False,
        description='always control camera when not touching selected object'
    )
    toggle_position: FloatVectorProperty(
        name='Toggle Position',
        subtype='XYZ',
        default=(0.5, 0.5, 0.0)
    )
    toggle_color: FloatVectorProperty(
        name='Toggle Button Color',
        default=(0.1, 0.1, 0.2, 0.5),
        subtype='COLOR',
        min=0.0,
        max=1.0,
        size=4,
    )

    isVisible: BoolProperty(name='Show Overlay', default=False)

    input_mode: EnumProperty(
        items=[
            ('full', 'full', 'mouse/touch and pen input'),
            ('pen', 'pen', 'pen input only'),
            ('touch', 'touch', 'mouse/touch input only')
        ],
        name='Input Mode',
        default='full'
    )

    enable_double_click: BoolProperty(
        name='Enable Double Click', default=True
    )
    double_click_mode: EnumProperty(
        items=double_click_items,
        name='Double Click Mode',
        default='screen.screen_full_area'
    )

    enable_right_click: BoolProperty(name='Enable Right Click', default=True)
    right_click_mode: EnumProperty(
        items=double_click_items,
        name='Right Click Mode',
        default='wm.window_fullscreen_toggle'
    )
    right_click_source: EnumProperty(
        items=[
            ('none', 'none', 'disabled'),
            ('mouse', 'mouse', 'mouse/touch right click'),
            ('pen', 'pen', 'pen right click')
        ],
        name='Right Click Source',
        default='mouse'
    )

    swap_panrotate: BoolProperty(name='Swap Pan/Rotate', default=False)

    width: FloatProperty(name='Width', default=40.0, min=10.0, max=100)
    radius: FloatProperty(name='Radius', default=35.0, min=10.0, max=100.0)

    use_multiple_colors: BoolProperty(name='Multicolor Overlay', default=False)
    overlay_main_color: FloatVectorProperty(
        name='Overlay Main Color',
        default=(1.0, 1.0, 1.0, 0.01),
        subtype='COLOR',
        min=0.0,
        max=1.0,
        size=4,
    )
    overlay_secondary_color: FloatVectorProperty(
        name='Overlay Secondary Color',
        default=(1.0, 1.0, 1.0, 0.01),
        subtype='COLOR',
        min=0.0,
        max=1.0,
        size=4,
    )

    ##
    # Gizmo Options
    ##
    show_menu: BoolProperty(name='Toggle Menu Display', default=True)
    show_gizmos: BoolProperty(name='Toggle Gizmos on Menu', default=True)
    menu_style: EnumProperty(
        name='Menu Style', default='float.radial', items=menu_style_items
    )
    menu_orientation: EnumProperty(
        name='Menu Orientation',
        default='HORIZONTAL',
        items=menu_orientation_items
    )
    menu_spacing: FloatProperty(
        name='Menu Size',
        default=20.0,
        precision=2,
        step=1,
        min=0.0,
        max=200.0
    )
    gizmo_padding: FloatProperty(
        name='Gizmo Padding', default=10, precision=1, step=1, min=1, max=200
    )
    gizmo_scale: FloatProperty(
        name='Gizmo Scale', default=4.0, precision=2, step=1, min=1, max=10.0
    )
    menu_position: FloatVectorProperty(
        name='Menu Position',
        default=(95.00, 5.00),
        size=2, precision=2,
        step=1,
        soft_min=5,
        soft_max=100
    )

    show_undoredo: BoolProperty(name='Undo/Redo', default=True)
    show_is_enabled: BoolProperty(name='Toggle Touch', default=True)
    show_control_gizmo: BoolProperty(name='Toggle Control Gizmo', default=True)
    show_show_fullscreen: BoolProperty(name='Fullscreen', default=True)
    show_region_quadviews: BoolProperty(name='Quadview', default=True)
    show_pivot_mode: BoolProperty(name='Pivot Mode', default=True)
    show_snap_view: BoolProperty(name='Snap View', default=True)
    show_n_panel: BoolProperty(name='N Panel', default=True)
    show_lock_rotation: BoolProperty(name='Rotation Lock', default=True)
    show_multires: BoolProperty(name='Multires', default=True)
    show_voxel_remesh: BoolProperty(name='Voxel Remesh', default=True)
    show_brush_dynamics: BoolProperty(name='Brush Dynamics', default=True)
    gizmo_position: EnumProperty(
        items=position_items,
        name='Gizmo Position',
        default='RIGHT'
    )
    subdivision_limit: IntProperty(
        name='Subdivision Limit',
        default=4,
        min=1,
        max=7
    )
    pivot_mode: EnumProperty(
        name='Sculpt Pivot Mode',
        items=pivot_items,
        default='SURFACE'
    )

    ##
    # Topology Control
    ##
    topology_mode: EnumProperty(
        name="Topology Mode",
        items=[
            ("MANUAL", "manual", "user-defined vertex density"),
            ("RELATIVE", "relative", "relative mesh vertex density steps"),
            (
                "RELATIVE-EXP",
                "exponential",
                "relative mesh vertex density steps with scaling"
            ),
        ],
        default="MANUAL"
    )

    ##
    # Action Menu Options
    ##
    show_float_menu: BoolProperty(name='Enable Floating Menu', default=False)
    floating_position: FloatVectorProperty(
        name='Floating Offset',
        default=(95.00, 5.00),
        size=2,
        precision=2,
        step=1,
        soft_min=5,
        soft_max=100
    )

    double_click_mode: EnumProperty(
        items=double_click_items,
        name='Double Click Mode',
        default='wm.window_fullscreen_toggle'
    )
    menu_sets: CollectionProperty(type=MenuModeGroup, options={'LIBRARY_EDITABLE'})

    ##
    # UI Panel Controls
    ##
    active_menu: EnumProperty(name='Mode Settings', items=edit_modes)
    gizmo_tabs: EnumProperty(name='Gizmo Tabs', items=[
        ('MENU', 'Gizmo Menu', '', 0),
        ('ACTIONS', 'Action Menu', '', 1)
    ], default='MENU')

    # set up addon preferences UI
    def draw(self, _: Context):
        # Input Mode
        col = self.layout.column()
        col.label(text='Input Mode')
        col = col.box()
        if self.input_mode == 'full':
            col.label(text='pen, mouse, touch input', icon='CON_CAMERASOLVER')
        if self.input_mode == 'pen':
            col.label(text='pen-only input', icon='STYLUS_PRESSURE')
        if self.input_mode == 'touch':
            col.label(text='mouse/touch only input', icon='VIEW_PAN')
        tabs = col.column_flow(columns=3, align=True)
        tabs.prop_tabs_enum(self, 'input_mode')
        col.prop(self, 'lazy_mode', toggle=1)

        # main settings
        row = self.layout.split(factor=0.4)
        ##
        # Viewport Settings
        ##
        col = row.column()
        col.label(text='Control Zones')
        col.label(text='Input Mode')
        col.prop(self, 'is_enabled', toggle=1)
        col.prop(self, 'swap_panrotate')
        col.prop(self, 'isVisible', text='Show Overlay')
        col.prop(self, 'use_multiple_colors')
        col.prop(self, 'overlay_main_color', text='Main Color')
        if self.use_multiple_colors:
            col.prop(self, 'overlay_secondary_color', text='Secondary Color')
        col.prop(self, 'width', slider=True)
        col.prop(self, 'radius', slider=True)

        ##
        # Gizmo Settings
        ##
        col = row.column()
        col.label(text='Gizmo Options')
        tabs = col.column_flow(columns=3, align=True)
        tabs.prop_tabs_enum(self, 'gizmo_tabs')

        main = col.box()
        if self.gizmo_tabs == 'MENU':
            main.label(text='Gizmo Menu Style')
            tabs = main.column_flow(columns=2, align=True)
            tabs.prop_tabs_enum(self, 'menu_style')

            if self.menu_style == 'fixed.bar':
                main.prop_menu_enum(self, 'gizmo_position')
            main.prop(self, 'menu_spacing', slider=True)
            if self.menu_style == 'float.radial':
                main.prop(self, 'gizmo_padding', slider=True)
            main.prop(self, 'gizmo_scale', slider=True)

            main.separator()
            main.label(text='Input Options')
            wrapper = main.box()
            wrapper.label(text='Right Click Actions')
            r = wrapper.split(factor=0.3, align=True)
            r.label(text='Input Source')
            r = r.row()
            r.prop(self, 'right_click_source', expand=True)

            r = wrapper.split(factor=0.3, align=True)
            r.label(text='Click Action')
            c = r.column()
            c.prop(self, 'right_click_mode', expand=True)
            main.separator()
            wrapper = main.box()
            wrapper.label(text='Double Click Actions')
            wrapper.prop(self, 'enable_double_click', toggle=1)
            r = wrapper.split(factor=0.3, align=True)
            r.label(text='Click Action')
            c = r.column()
            c.prop(self, 'double_click_mode', expand=True)

            main.separator()
            main.label(text='Tool Settings')
            main.prop(self, 'subdivision_limit', slider=True)

        if self.gizmo_tabs == 'ACTIONS':
            if not self.show_float_menu:
                main.operator(
                    'view3d.toggle_floating_menu',
                    text='Show Action Menu'
                )
            else:
                main.operator(
                    'view3d.toggle_floating_menu',
                    text='Hide Action Menu',
                    depress=True
                )
                box = main.box()
                box.active = self.show_float_menu
                main = box.column()
                main.prop(self, 'active_menu')
                mList = self.getMenuSettings(self.active_menu)
                for i in range(7):
                    main.prop(mList, 'menu_slot_' + str(i + 1))

    ##
    # Data Accessors
    ##
    def getMenuSettings(self, mode: str):
        m = None
        for opts in self.menu_sets:
            if opts.mode == mode:
                m = opts
        if m is None:
            m = self.menu_sets.add()
            m.mode = mode
            ops = menu_defaults[mode]
            for i, o in enumerate(ops):
                setattr(m, 'menu_slot_' + str(i + 1), o)
        return m

    def getGizmoSet(self, mode: str | int):
        available = list(gizmo_sets['ALL'])

        if mode not in list(gizmo_sets):
            return available
        return available + list(gizmo_sets[mode])

    def getShowLock(self):
        return self.show_lock

    def getWidth(self):
        return self.width / 100

    def getRadius(self):
        return self.radius / 100

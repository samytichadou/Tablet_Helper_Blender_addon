import bpy
import os

addon_name = os.path.basename(os.path.dirname(__file__))

        
# get addon preferences
def get_addon_preferences():
    addon = bpy.context.preferences.addons.get(addon_name)
    return getattr(addon, "preferences", None)

def update_sidepanel_category(self, context):
    from .gui import TABLETH_PT_actions_panel as panel
    bpy.utils.unregister_class(panel)
    panel.bl_category = get_addon_preferences().sidebar_panel_category
    bpy.utils.register_class(panel)


class TABLETH_PT_addon_prefs(bpy.types.AddonPreferences):
    bl_idname = addon_name

    save_folder : bpy.props.StringProperty(
        name = 'Save Folder',
        default = "",
        subtype = "DIR_PATH",
        )
    
    topbar_menu : bpy.props.BoolProperty(
        name = 'Topbar Menu', 
        default = True
        )

    sidebar_panel : bpy.props.BoolProperty(
        name = 'Sidebar Panel', 
        )

    sidebar_panel_category : bpy.props.StringProperty(
        name = 'Category',
        default = "TabletH",
        update=update_sidepanel_category,
        )

    widget_menu : bpy.props.BoolProperty(
        name = 'Widget', 
        )

    popup_menu : bpy.props.BoolProperty(
        name = 'Popup Menu', 
        )

    def draw(self, context):       
        layout = self.layout

        layout.prop(self, "save_folder")

        col=layout.column(align=True)
        row=col.row(align=True)
        row.prop(self, "sidebar_panel")
        row=row.row()
        if not self.sidebar_panel:
            row.enabled=False
        row.prop(self, "sidebar_panel_category")
        col.prop(self, "topbar_menu")
        col.prop(self, "widget_menu")
        col.prop(self, "popup_menu")

        # donate
        op=layout.operator("wm.url_open", text="Donate", icon="FUND")
        op.url="https://ko-fi.com/tonton_blender"


### REGISTER ---

def register():
    bpy.utils.register_class(TABLETH_PT_addon_prefs)

def unregister():
    bpy.utils.unregister_class(TABLETH_PT_addon_prefs)
import bpy
import os

addon_name = os.path.basename(os.path.dirname(__file__))

class TABLETH_PT_addon_prefs(bpy.types.AddonPreferences):
    bl_idname = addon_name
    
    topbar_menu : bpy.props.BoolProperty(
        name = 'Topbar Menu', 
        )

    sidebar_panel : bpy.props.BoolProperty(
        name = 'Sidebar Panel', 
        )

    widget_menu : bpy.props.BoolProperty(
        name = 'widget', 
        )

    popup_panel : bpy.props.BoolProperty(
        name = 'Sidebar Panel', 
        )

    def draw(self, context):       
        layout = self.layout

        row=layout.row(align=True)
        row.prop(self, "topbar_menu")
        row.prop(self, "sidebar_panel")
        row.prop(self, "widget_menu")
        row.prop(self, "popup_panel")

        # donate
        op=layout.operator("wm.url_open", text="Donate", icon="FUND")
        op.url="https://ko-fi.com/tonton_blender"

        
# get addon preferences
def get_addon_preferences():
    addon = bpy.context.preferences.addons.get(addon_name)
    return getattr(addon, "preferences", None)


### REGISTER ---

def register():
    bpy.utils.register_class(TABLETH_PT_addon_prefs)

def unregister():
    bpy.utils.unregister_class(TABLETH_PT_addon_prefs)
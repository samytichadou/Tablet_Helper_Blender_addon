import bpy

from .addons_prefs import get_addon_preferences


def draw_gui(context, container):
    commands = context.scene.tableth_commands
    if commands:
        col=container.column(align=True)
        for c in commands:
            if c.icon:
                try:
                    op=col.operator("tableth.execute_command", text=c.name, icon=c.icon)
                except TypeError:
                    op=col.operator("tableth.execute_command", text=c.name)
            else:
                op=col.operator("tableth.execute_command", text=c.name)
            op.command_name=c.name
    else:
        container.label(text="No commands", icon="INFO")
    container.operator("tableth.manage_commands_popup", text="Commands", icon="SETTINGS")


# SIDEBAR PANEL
class TABLETH_PT_commands_panel(bpy.types.Panel):
    bl_label = "Commands"
    bl_space_type = "VIEW_3D"
    bl_region_type = "UI"
    bl_category = "Tablet H"

    @classmethod
    def poll(cls, context):
        return get_addon_preferences().sidebar_panel

    def draw(self, context):
        layout = self.layout
        draw_gui(context, layout)


# MANAGE MENU
class TABLETH_OT_manage_commands_popup(bpy.types.Operator):
    bl_idname = "tableth.manage_commands_popup"
    bl_label = "Manage Commands"
    #bl_description = ""
    #bl_options = {"UNDO"}

    tmp_name : bpy.props.StringProperty(name="Name", default="New Command")
    tmp_command : bpy.props.StringProperty(name="Command", default="bpy.ops.")
    tmp_description : bpy.props.StringProperty(name="Description")
    tmp_context : bpy.props.StringProperty(name="Context")
    tmp_icon : bpy.props.StringProperty(name="Icon")


    @classmethod
    def poll(cls, context):
        return True

    def invoke(self, context, event):
        return context.window_manager.invoke_props_dialog(self)

    def draw(self, context):
        layout = self.layout
        commands = context.scene.tableth_commands

        # Create
        box=layout.box()
        col=box.column(align=True)
        col.label(text="Create New Command")
        col.prop(self,"tmp_name")
        col.prop(self,"tmp_command")
        col.prop(self,"tmp_description")
        col.prop(self,"tmp_context")
        col.prop(self,"tmp_icon")
        op=col.operator("tableth.create_command", text="Create")
        op.tmp_name=self.tmp_name
        op.tmp_command=self.tmp_command
        op.tmp_description=self.tmp_description
        op.tmp_context=self.tmp_context
        op.tmp_icon=self.tmp_icon

        # Lits
        box=layout.box()
        col=box.column(align=True)
        col.label(text="Lists")
        for c in commands:
            col.label(text=c.name) 

    def execute(self, context):
        return {'FINISHED'}


### REGISTER ---

def register():
    bpy.utils.register_class(TABLETH_PT_commands_panel)
    bpy.utils.register_class(TABLETH_OT_manage_commands_popup)

def unregister():
    bpy.utils.unregister_class(TABLETH_PT_commands_panel)
    bpy.utils.unregister_class(TABLETH_OT_manage_commands_popup)
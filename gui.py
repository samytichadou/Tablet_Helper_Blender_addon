from re import sub
import bpy

from .addons_prefs import get_addon_preferences


def draw_gui(context, container):
    commands = context.scene.tableth_actions
    if commands:
        col=container.column(align=True)
        idx=0
        for c in commands:
            if c.icon:
                try:
                    op=col.operator("tableth.execute_action", text=c.name, icon=c.icon)
                except TypeError:
                    op=col.operator("tableth.execute_action", text=c.name)
            else:
                op=col.operator("tableth.execute_action", text=c.name)
            op.index=idx
            idx+=1
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

    tmp_name : bpy.props.StringProperty(name="Name", default="New Action")
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
        scn = context.scene
        actions = scn.tableth_actions
        active_action = actions[scn.tableth_action_index]

        # Create
        box=layout.box()
        col=box.column(align=True)
        op=col.operator("tableth.create_action", text="Create Action", icon="PLUS")
        op.tmp_name=self.tmp_name
        op.tmp_description=self.tmp_description
        op.tmp_context=self.tmp_context
        op.tmp_icon=self.tmp_icon
        col.prop(self,"tmp_name")
        col.prop(self,"tmp_description")
        col.prop(self,"tmp_context")
        col.prop(self,"tmp_icon")

        # List
        box=layout.box()
        col=box.column(align=True)
        col.label(text="Actions")
        col.template_list("TABLETH_UL_action_slots", "", scn, "tableth_actions", scn, "tableth_action_index", rows=4)
        subbox=box.box()
        col=subbox.column(align=True)
        col.prop(active_action, "name")
        col.prop(active_action, "description")
        col.prop(active_action, "context")
        col.prop(active_action, "icon")
        # Command list
        idx = active_action.command_index
        row=col.row(align=True)
        row.template_list("TABLETH_UL_command_slots", "", active_action, "commands", active_action, "command_index", rows=3)
        col=row.column(align=True)
        col.operator("tableth.manage_commands",text="",icon="ADD").action="ADD"
        col.operator("tableth.manage_commands",text="",icon="REMOVE").action="REMOVE"
        col.operator("tableth.manage_commands",text="",icon="TRIA_UP").action="UP"
        col.operator("tableth.manage_commands",text="",icon="TRIA_DOWN").action="DOWN"

        if idx!=-1 and idx<len(active_action.commands):
            active_command = active_action.commands[idx]
            col.prop(active_command, "command")

    def execute(self, context):
        return {'FINISHED'}


### REGISTER ---

def register():
    bpy.utils.register_class(TABLETH_PT_commands_panel)
    bpy.utils.register_class(TABLETH_OT_manage_commands_popup)

def unregister():
    bpy.utils.unregister_class(TABLETH_PT_commands_panel)
    bpy.utils.unregister_class(TABLETH_OT_manage_commands_popup)
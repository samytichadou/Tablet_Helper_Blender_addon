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
    container.operator("tableth.manage_commands_popup", text="Commands", icon="TOOL_SETTINGS")


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

    @classmethod
    def poll(cls, context):
        return True

    def invoke(self, context, event):
        return context.window_manager.invoke_props_dialog(self)

    def draw(self, context):
        layout = self.layout
        scn = context.scene
        actions = scn.tableth_actions
        active_action = None
        action_idx = scn.tableth_action_index

        if action_idx!=-1 and action_idx<len(actions):
            active_action = actions[scn.tableth_action_index]

        # List
        box=layout.box()
        col=box.column(align=True)
        col.label(text="Actions", icon="MEMORY")
        row=col.row(align=False)
        row.template_list("TABLETH_UL_action_slots", "", scn, "tableth_actions", scn, "tableth_action_index", rows=4)
        subcol=row.column(align=True)
        subcol.operator("tableth.manage_actions",text="",icon="ADD").action="ADD"
        subcol.operator("tableth.manage_actions",text="",icon="REMOVE").action="REMOVE"
        subcol.operator("tableth.manage_actions",text="",icon="TRIA_UP").action="UP"
        subcol.operator("tableth.manage_actions",text="",icon="TRIA_DOWN").action="DOWN"

        if active_action:
            subbox=box.box()
            subbox.label(text="Action Settings", icon="SETTINGS")
            col=subbox.column(align=True)
            col.prop(active_action, "name")
            col.prop(active_action, "description")
            col.prop(active_action, "context")
            col.prop(active_action, "icon")
            # Command list
            idx = active_action.command_index
            col.separator()
            col.label(text="Commands Settings", icon="FILE_SCRIPT")
            row=col.row(align=False)
            row.template_list("TABLETH_UL_command_slots", "", active_action, "commands", active_action, "command_index", rows=3)
            subcol=row.column(align=True)
            subcol.operator("tableth.manage_commands",text="",icon="ADD").action="ADD"
            subcol.operator("tableth.manage_commands",text="",icon="REMOVE").action="REMOVE"
            subcol.operator("tableth.manage_commands",text="",icon="TRIA_UP").action="UP"
            subcol.operator("tableth.manage_commands",text="",icon="TRIA_DOWN").action="DOWN"

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
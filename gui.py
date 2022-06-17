from re import sub
import bpy

from .addons_prefs import get_addon_preferences


def draw_gui(context, container):
    scn = context.scene
    commands = scn.tableth_actions
    if commands:
        col=container.column(align=True)
        idx=0
        for c in commands:
            row=col.row(align=True)
            if scn.tableth_recording!=-1:
                if scn.tableth_recording==idx:
                    row.alert=True
                    op=row.operator("tableth.recording", text="", icon="REC")
                    op.action="STOP"
                    op=row.operator("tableth.recording", text="", icon="LOOP_BACK")
                    op.action="RESET"
                    row=row.row()
                    row.enabled=False
            if c.icon:
                try:
                    op=row.operator("tableth.execute_action", text=c.name, icon=c.icon)
                except TypeError:
                    op=row.operator("tableth.execute_action", text=c.name)
            else:
                op=row.operator("tableth.execute_action", text=c.name)
            op.index=idx
            idx+=1
    else:
        container.label(text="No commands", icon="INFO")
    container.operator("tableth.manage_commands_popup", text="Manage", icon="TOOL_SETTINGS")


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
            col=subbox.column(align=True)
            col.label(text="Action Settings", icon="SETTINGS")
            col.separator()
            col.prop(active_action, "name")
            col.prop(active_action, "description")
            col.prop(active_action, "context")
            col.prop(active_action, "icon")

            # Command list
            idx = active_action.command_index
            col.separator()
            col.label(text="Commands Settings", icon="FILE_SCRIPT")
            col.separator()

            row=col.row(align=True)
            if scn.tableth_recording==-1:
                text="Start Recording"
                action="START"
            else:
                text="Stop Recording"
                action="STOP"
            op=row.operator("tableth.recording", text=text, icon="REC")
            op.index=action_idx
            op.action=action
            if scn.tableth_recording!=-1:
                op=row.operator("tableth.recording", text="", icon="LOOP_BACK")
                op.action="RESET"

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
                col.prop(active_command, "name")

    def execute(self, context):
        return {'FINISHED'}


### REGISTER ---

def register():
    bpy.utils.register_class(TABLETH_PT_commands_panel)
    bpy.utils.register_class(TABLETH_OT_manage_commands_popup)

def unregister():
    bpy.utils.unregister_class(TABLETH_PT_commands_panel)
    bpy.utils.unregister_class(TABLETH_OT_manage_commands_popup)
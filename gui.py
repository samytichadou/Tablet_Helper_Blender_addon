from re import sub
import bpy

from .addons_prefs import get_addon_preferences, update_sidepanel_category

# COMMON ACTION GUI
def draw_gui(context, container, type):
    scn = context.scene
    props = scn.tableth_properties
    actions = props.actions
    idx=None
    if actions:
        idx=0
        col=container.column(align=True)
        for a in actions:
            # Check contexts
            if a.context_mode:
                if not a.context_mode==context.mode:
                    continue
            if a.context_active_type:
                if context.active_object:
                    if not a.context_active_type==context.active_object.type:
                        continue
                else:
                    continue
            if a.context_workspace:
                if not a.context_workspace==context.workspace.name:
                    continue
            if a.context_location=="SPECIFIC":
                if type not in a.context_specific_location.lower():
                    continue
            elif a.context_location!="ALL" and a.context_location.lower()!=type:
                continue 
            
            # Display Operators
            row=col.row(align=True)
            if props.recording!=-1:
                if props.recording==idx:
                    row.alert=True
                    op=row.operator("tableth.recording", text="", icon="REC")
                    op.action="STOP"
                    op=row.operator("tableth.recording", text="", icon="LOOP_BACK")
                    op.action="RESET"
                    row=row.row()
                    row.enabled=False
            if a.icon:
                try:
                    op=row.operator("tableth.execute_action", text=a.name, icon=a.icon)
                except TypeError:
                    op=row.operator("tableth.execute_action", text=a.name)
            else:
                op=row.operator("tableth.execute_action", text=a.name)
            op.index=idx
            idx+=1
    if not idx or idx==0:
        container.label(text="No Actions", icon="INFO")
    container.operator("tableth.manage_commands_popup", text="Manage", icon="TOOL_SETTINGS")


# SIDEBAR ACTION PANEL
class TABLETH_PT_actions_panel(bpy.types.Panel):
    bl_label = "Actions"
    bl_space_type = "VIEW_3D"
    bl_region_type = "UI"
    bl_category = "TabletH"

    @classmethod
    def poll(cls, context):
        return get_addon_preferences().sidebar_panel

    def draw_header(self, context):
        self.layout.label(text="", icon="MEMORY")

    def draw(self, context):
        layout = self.layout
        draw_gui(context, layout, "sidebar")


# POPOVER ACTION PANEL
class TABLETH_PT_actions_popover(bpy.types.Panel):
    bl_label = "Actions"
    bl_options = {'INSTANCED'}
    bl_space_type = "VIEW_3D"
    bl_region_type = 'WINDOW'

    @classmethod
    def poll(cls, context):
        return get_addon_preferences().topbar_menu

    def draw(self, context):
        layout = self.layout
        draw_gui(context, layout, "topbar")


# POPOVER ACTION CALLER
def popover_menu(self, context):
    if get_addon_preferences().topbar_menu:
        layout = self.layout
        layout.popover("TABLETH_PT_actions_popover", text="", icon="MEMORY")


# POPUP ACTION MENU
class TABLETH_OT_actions_popup(bpy.types.Operator):
    bl_idname = "tableth.action_popup"
    bl_label = "Actions"
    #bl_description = ""
    #bl_options = {"UNDO"}

    @classmethod
    def poll(cls, context):
        return get_addon_preferences().popup_menu

    def invoke(self, context, event):
        return context.window_manager.invoke_props_dialog(self)

    def draw(self, context):
        layout = self.layout
        draw_gui(context, layout, "popup")

    def execute(self, context):
        return {'FINISHED'}


# POPUP MANAGE MENU 
class TABLETH_OT_manage_commands_popup(bpy.types.Operator):
    bl_idname = "tableth.manage_commands_popup"
    bl_label = "Manage Commands"
    #bl_description = ""
    #bl_options = {"UNDO"}

    show_context : bpy.props.BoolProperty(
        name="Show Context Details",
        )

    @classmethod
    def poll(cls, context):
        return True

    def invoke(self, context, event):
        return context.window_manager.invoke_props_dialog(self)

    def draw(self, context):
        layout = self.layout
        scn = context.scene
        props = scn.tableth_properties
        actions = props.actions
        active_action = None
        action_idx = props.action_index

        if action_idx!=-1 and action_idx<len(actions):
            active_action = actions[props.action_index]

        # List
        box=layout.box()
        col=box.column(align=True)
        col.label(text="Actions", icon="MEMORY")
        row=col.row(align=False)
        row.template_list("TABLETH_UL_action_slots", "", props, "actions", props, "action_index", rows=4)
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
            col.prop(active_action, "icon")
            subbox2=col.box()
            subcol=subbox2.column(align=True)
            if self.show_context:
                icon="TRIA_DOWN"
            else:
                icon="TRIA_RIGHT"
            row=subcol.row(align=True)
            row.prop(self, "show_context", text="", icon=icon, emboss=False)
            row.label(text="Context")
            if self.show_context:
                subcol.prop(active_action, "context_mode", text="Mode")
                subcol.prop(active_action, "context_active_type", text="Active Type")
                subcol.prop(active_action, "context_workspace", text="Workspace")
                subcol.prop(active_action, "context_location", text="Location")
                row=subcol.row()
                if active_action.context_location!="SPECIFIC":
                    row.enabled=False
                row.prop(active_action, "context_specific_location", text="Specific")

            # Command list
            idx = active_action.command_index
            col.separator()
            col.label(text="Commands Settings", icon="FILE_SCRIPT")
            col.separator()

            row=col.row(align=True)
            if props.recording==-1:
                text="Start Recording"
                action="START"
            else:
                text="Stop Recording"
                action="STOP"
            op=row.operator("tableth.recording", text=text, icon="REC")
            op.index=action_idx
            op.action=action
            if props.recording!=-1:
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
    bpy.utils.register_class(TABLETH_PT_actions_panel)
    update_sidepanel_category(None, bpy.context)
    bpy.utils.register_class(TABLETH_PT_actions_popover)
    bpy.utils.register_class(TABLETH_OT_actions_popup)
    bpy.utils.register_class(TABLETH_OT_manage_commands_popup)
    bpy.types.VIEW3D_HT_header.append(popover_menu)

def unregister():
    bpy.utils.unregister_class(TABLETH_PT_actions_panel)
    bpy.utils.unregister_class(TABLETH_PT_actions_popover)
    bpy.utils.unregister_class(TABLETH_OT_actions_popup)
    bpy.utils.unregister_class(TABLETH_OT_manage_commands_popup)
    bpy.types.VIEW3D_HT_header.remove(popover_menu)
import bpy


commands_to_avoid = {
    "bpy.ops.text.run_script()",
    "Python script failed, check the message in the system console",
    "Record",
    "Saved",
}

def set_override(context):
    win = context.window_manager.windows[0]
    area = win.screen.areas[0]
    old_area = area.type
    area.type = 'INFO'
    override = bpy.context.copy()
    override['window'] = win
    override['screen'] = win.screen
    override['area'] = win.screen.areas[0]
    return override, old_area


class TABLETH_OT_recording(bpy.types.Operator):
    bl_idname = "tableth.recording"
    bl_label = "Start/Stop/Reset Recording"

    action : bpy.props.EnumProperty(items=(
        ('START', 'Start', ""),
        ('STOP', 'Stop', ""),
        ('RESET', 'Reset', ""),
        ))
    index : bpy.props.IntProperty()

    @classmethod
    def poll(cls, context):
        scn = context.scene
        action_idx = scn.tableth_action_index
        actions = scn.tableth_actions
        return action_idx!=-1 and action_idx<len(actions)

    def execute(self, context):
        scn=context.scene
        action=scn.tableth_actions[self.index]

        override, old_area = set_override(context)

        if self.action=="START":
            # Clear infos
            bpy.ops.info.select_all(override, action='SELECT')
            bpy.ops.info.report_delete(override)
            bpy.ops.info.select_all(override, action='DESELECT')

            scn.tableth_recording=self.index
            self.report({'INFO'}, "Recording : %s" % action.name)

        elif self.action=="STOP":
            # Rec infos
            bpy.ops.info.select_all(override, action='SELECT')
            bpy.ops.info.report_copy(override)
            bpy.ops.info.select_all(override, action='DESELECT')
            # Create commands
            for line in context.window_manager.clipboard.splitlines():
                chk_avoid=0
                for a in commands_to_avoid:
                    if a in line:
                        chk_avoid=1
                        break
                if chk_avoid:
                    print("Record avoided for command - %s" % line)
                    continue
                new_command=action.commands.add()
                new_command.command=line

            scn.tableth_recording=-1
            self.report({'INFO'}, "Recorded : %s" % action.name)

        elif self.action=="RESET" and scn.tableth_recording!=-1:
            # Rec infos
            bpy.ops.info.select_all(override, action='SELECT')
            bpy.ops.info.report_delete(override)
            bpy.ops.info.select_all(override, action='DESELECT')
            self.report({'INFO'}, "Recording Reset")
        
        context.window_manager.windows[0].screen.areas[0].type=old_area

        # redraw ui
        for area in context.screen.areas:
            area.tag_redraw()

        return {'FINISHED'}

### REGISTER ---

def register():
    bpy.utils.register_class(TABLETH_OT_recording)

def unregister():
    bpy.utils.unregister_class(TABLETH_OT_recording)
import bpy


class TABLETH_create_command(bpy.types.Operator):
    bl_idname = "tableth.create_command"
    bl_label = "Create Command"

    tmp_name : bpy.props.StringProperty(name="Name")
    tmp_command : bpy.props.StringProperty(name="Command")
    tmp_description : bpy.props.StringProperty(name="Description")
    tmp_context : bpy.props.StringProperty(name="Context")
    tmp_icon : bpy.props.StringProperty(name="Context")

    @classmethod
    def poll(cls, context):
        return True

    def execute(self, context):
        if not self.tmp_name or not self.tmp_command:
            self.report({'WARNING'}, "Missing Name or Command")
            return {'FINISHED'}

        commands=context.scene.tableth_commands
        for c in commands:
            if c.name==self.tmp_name:
                self.report({'WARNING'}, "Command %s already exists" % self.name)
                return {'FINISHED'}

        new_command=commands.add()
        new_command.name=self.tmp_name
        new_command.command=self.tmp_command
        new_command.description=self.tmp_description
        new_command.context=self.tmp_context
        new_command.icon=self.tmp_icon

        self.report({'INFO'}, "Command %s created" % self.name)

        # redraw ui
        for area in context.screen.areas:
            area.tag_redraw()

        return {'FINISHED'}


### REGISTER ---

def register():
    bpy.utils.register_class(TABLETH_create_command)

def unregister():
    bpy.utils.unregister_class(TABLETH_create_command)
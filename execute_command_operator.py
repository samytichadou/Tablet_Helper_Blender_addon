import bpy


class TABLETH_execute_command(bpy.types.Operator):
    bl_idname = "tableth.execute_command"
    bl_label = "Execute Command"

    command_name : bpy.props.StringProperty(name="Name")

    @classmethod
    def poll(cls, context):
        return True

    def execute(self, context):
        commands=context.scene.tableth_commands

        command=commands[self.command_name]

        exec(command.command)

        self.report({'INFO'}, "%s Executed" % self.command_name)

        return {'FINISHED'}


### REGISTER ---

def register():
    bpy.utils.register_class(TABLETH_execute_command)

def unregister():
    bpy.utils.unregister_class(TABLETH_execute_command)
import bpy


class TABLETH_create_action(bpy.types.Operator):
    bl_idname = "tableth.create_action"
    bl_label = "Create Command"

    tmp_name : bpy.props.StringProperty(name="Name")
    tmp_description : bpy.props.StringProperty(name="Description")
    tmp_context : bpy.props.StringProperty(name="Context")
    tmp_icon : bpy.props.StringProperty(name="Context")

    @classmethod
    def poll(cls, context):
        return True

    def execute(self, context):
        if not self.tmp_name:
            self.report({'WARNING'}, "Missing Name")
            return {'FINISHED'}

        actions=context.scene.tableth_actions
        for c in actions:
            if c.name==self.tmp_name:
                self.report({'WARNING'}, "Action %s already exists" % self.name)
                return {'FINISHED'}

        new_action=actions.add()
        new_action.name=self.tmp_name
        new_action.description=self.tmp_description
        new_action.context=self.tmp_context
        new_action.icon=self.tmp_icon

        self.report({'INFO'}, "Command %s created" % self.name)

        # redraw ui
        for area in context.screen.areas:
            area.tag_redraw()

        return {'FINISHED'}


### REGISTER ---

def register():
    bpy.utils.register_class(TABLETH_create_action)

def unregister():
    bpy.utils.unregister_class(TABLETH_create_action)
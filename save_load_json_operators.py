import bpy
import json
import os
import pathlib

from .addons_prefs import get_addon_preferences


# check if serializable
def isSerializable(x):
    try:
        json.dumps(x)
        return True
    except (TypeError, OverflowError):
        return False

def dataset_from_properties(datasetin, avoid_list=()):
    datasetout = {}
    for p in datasetin.bl_rna.properties:
        if p.identifier not in avoid_list:
            if not p.is_readonly:
                if isSerializable(getattr(datasetin, p.identifier)):
                    datasetout[p.identifier] = getattr(datasetin, p.identifier)
    return datasetout

def return_action_dataset(action):
    datasetout=dataset_from_properties(action)
    datasetout["commands"]=[]
    for c in action.commands:
        json_command=dataset_from_properties(c)
        datasetout["commands"].append(json_command)
    return datasetout

def return_action_filename(name, index):
    return "action%s_%s.json" % (str(index).zfill(3), name)

def create_json_file(datas, path) :
    with open(path, "w") as write_file :
        json.dump(datas, write_file, indent=4, sort_keys=False)

def empty_directory(directory, include_pattern=None):
    for root, dirs, files in os.walk(directory):
        for file in files:
            if include_pattern is not None:
                if include_pattern in file:
                    os.remove(os.path.join(root, file))
            else:
                os.remove(os.path.join(root, file))


class TABLETH_OT_save_actions(bpy.types.Operator):
    bl_idname = "tableth.save_actions"
    bl_label = "Save Actions"

    @classmethod
    def poll(cls, context):
        scn = context.scene
        props = scn.tableth_properties
        return props.actions

    def execute(self, context):
        scn=context.scene
        props = scn.tableth_properties
        actions = props.actions

        save_folder = get_addon_preferences().save_folder
        # Create folder if needed
        if not os.path.isdir:
            pathlib.Path(save_folder).mkdir(parents=True, exist_ok=True)
        # Empty dir
        else:
            empty_directory(save_folder, "action")

        idx=0
        for a in actions:
            json_datas=return_action_dataset(a)
            file_name=return_action_filename(a.name, idx)
            path = os.path.join(save_folder, file_name)
            create_json_file(json_datas, path)
            idx+=1
        
        self.report({'INFO'}, "Actions Saved")

        return {'FINISHED'}


### REGISTER ---

def register():
    bpy.utils.register_class(TABLETH_OT_save_actions)

def unregister():
    bpy.utils.unregister_class(TABLETH_OT_save_actions)
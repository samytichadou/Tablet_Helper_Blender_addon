# set attributes between 2 dataset
def setPropertiesFromDataset(datasetin, datasetout):
    for prop in datasetin.bl_rna.properties:
        if not prop.is_readonly:
            try:
                setattr(datasetout, '%s' % prop.identifier, getattr(datasetin, prop.identifier))
            except (KeyError, AttributeError):
                print(g_var.setting_prop_error_statement + prop.identifier) #debug
                pass

# set attributes from json
def setPropertiesFromJsonDataset(datasetin, datasetout, debug, avoid_list):
    if debug: print(g_var.setting_prop_statement + str(datasetin)) #debug
    for prop in datasetin:
        chk_avoid = False
        for a in avoid_list:
            if a in prop:
                chk_avoid = True
        if not chk_avoid:
            try:
                setattr(datasetout, '%s' % prop, datasetin[prop])
            except (KeyError, AttributeError, TypeError):
                if debug: print(g_var.setting_prop_error_statement + prop) #debug
                pass
        else:
            if debug: print(g_var.prop_avoided_statement + prop)


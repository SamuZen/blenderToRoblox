import bpy

class PackagePropertyOperator(bpy.types.Operator):
    """Performs a custom operation"""
    bl_idname = "object.package_property_operator"
    bl_label = "Add Package Property"

    def execute(self, context):
        self.custom_function(context)
        return {'FINISHED'}

    def custom_function(self, context):
        # Adiciona a propriedade personalizada ao objeto ou coleção selecionada
        if context.object:
            context.object['Roblox Package ID'] = '112233'
        elif context.collection:
            context.collection['Roblox Package ID'] = '112233'

class PackageObjectPanel(bpy.types.Panel):
    """Creates a Panel in the Object properties window"""
    bl_label = "RBX PACKAGE Panel"
    bl_idname = "OBJECT_PT_package"
    bl_space_type = 'PROPERTIES'
    bl_region_type = 'WINDOW'
    bl_context = "object"

    def draw(self, context):
        layout = self.layout

        layout.label(text="Package:")
        row = layout.row()
        row.operator("object.package_property_operator")

class PackageCollectionPanel(bpy.types.Panel):
    """Creates a Panel in the Collection properties window"""
    bl_label = "RBX PACKAGE Panel"
    bl_idname = "COLLECTION_PT_package"
    bl_space_type = 'PROPERTIES'
    bl_region_type = 'WINDOW'
    bl_context = "collection"

    def draw(self, context):
        layout = self.layout

        layout.label(text="Package:")
        row = layout.row()
        row.operator("object.package_property_operator")

def register():
    bpy.utils.register_class(PackagePropertyOperator)
    bpy.utils.register_class(PackageObjectPanel)
    bpy.utils.register_class(PackageCollectionPanel)

def unregister():
    bpy.utils.unregister_class(PackagePropertyOperator)
    bpy.utils.unregister_class(PackageObjectPanel)
    bpy.utils.unregister_class(PackageCollectionPanel)

if __name__ == "__main__":
    register()

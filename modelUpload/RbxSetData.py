import bpy
import json
import math

# Função para adicionar ou modificar a propriedade 'Roblox Material' no objeto
def add_or_modify_roblox_material(obj, material_type):
    obj['Roblox Material'] = material_type

# Função para remover a propriedade 'Roblox Material' do objeto
def remove_roblox_material(obj):
    if 'Roblox Material' in obj:
        del obj['Roblox Material']

# Função para atualizar o label com o valor da propriedade 'Roblox Material'
def update_label(layout, obj):
    if 'Roblox Material' in obj:
        layout.label(text=f"Roblox Material: {obj['Roblox Material']}")
    else:
        layout.label(text="Roblox Material: N/A")

def to_hex(c):
    if c < 0.0031308:
        srgb = 0.0 if c < 0.0 else c * 12.92
    else:
        srgb = 1.055 * math.pow(c, 1.0 / 2.4) - 0.055
    return hex(max(min(int(srgb * 255 + 0.5), 255), 0))

def gamma_correct(color, gamma=2.2):
    return tuple(pow(c, 1.0 / gamma) for c in color[:3])

def color_to_hex(color):
    return "#{:02x}{:02x}{:02x}".format(
        int(color[0] * 255),
        int(color[1] * 255),
        int(color[2] * 255)
    )

class OBJECT_PT_RobloxMaterialPanel(bpy.types.Panel):
    bl_label = "Roblox Material Panel"
    bl_idname = "OBJECT_PT_roblox_material"
    bl_space_type = 'PROPERTIES'
    bl_region_type = 'WINDOW'
    bl_context = "object"

    def draw(self, context):
        layout = self.layout
        obj = context.object

        # Dropdown com opções de materiais
        layout.prop(obj, "roblox_material_dropdown", text="Material Type")

        # Botão para aplicar o material
        row = layout.row()
        row.operator("object.apply_roblox_material", text="Apply Material")

        # Botão para remover o material
        row = layout.row()
        row.operator("object.remove_roblox_material", text="Remove Material")

        # Label para mostrar o valor atual da propriedade 'Roblox Material'
        update_label(layout, obj)

        # Botão para aplicar dados JSON ao nome do objeto
        row = layout.row()
        row.operator("object.apply_data", text="Apply Data")

        # Botão para adicionar a propriedade de pacote
        row = layout.row()
        row.operator("object.package_property_operator", text="Add Package Property")

class OBJECT_OT_ApplyRobloxMaterial(bpy.types.Operator):
    bl_idname = "object.apply_roblox_material"
    bl_label = "Apply Roblox Material"

    def execute(self, context):
        obj = context.object
        material_type = obj.roblox_material_dropdown
        add_or_modify_roblox_material(obj, material_type)
        return {'FINISHED'}

class OBJECT_OT_RemoveRobloxMaterial(bpy.types.Operator):
    bl_idname = "object.remove_roblox_material"
    bl_label = "Remove Roblox Material"

    def execute(self, context):
        obj = context.object
        remove_roblox_material(obj)
        return {'FINISHED'}

class OBJECT_OT_ApplyData(bpy.types.Operator):
    bl_idname = "object.apply_data"
    bl_label = "Apply Data"

    def execute(self, context):
        selected_objects = context.selected_objects

        if len(selected_objects) > 0:
            print('SELECTED OBJECTS:')
            for obj in selected_objects:
                print('Object:', obj.name)
                
                data = {}
                        
                # Material
                if len(obj.material_slots) > 0:
                    first_material_slot = obj.material_slots[0]
                    if first_material_slot.material is not None:
                        material = first_material_slot.material
                        
                        # Base Color from Principled BSDF
                        if material.use_nodes:
                            for node in material.node_tree.nodes:
                                if node.type == 'BSDF_PRINCIPLED':
                                    base_color = node.inputs['Base Color'].default_value
                                    
                                    # Gamma correct
                                    gamma_corrected_color = gamma_correct(base_color, 2.2)
                                    
                                    # Convert gamma corrected color to hex format
                                    hex_color = color_to_hex(gamma_corrected_color)
                                    
                                    # Convert base color to hex format
                                    data["C"] = hex_color
                                    
                                    print(f"Base color (hex): {hex_color}")
                                    break
                        else:
                            data["C"] = None
                            print("Material does not use nodes")
                    else:
                        data["C"] = None
                        print("First material slot is empty")
                else:
                    data["C"] = None
                    print("No material slots available")

                # Check for 'Roblox Material' property
                if 'Roblox Material' in obj:
                    data["M"] = obj['Roblox Material']

                # Find clearName
                dataIndex = obj.name.find("{")
                dataEndIndex = obj.name.find("}")
                if dataIndex != -1 and dataEndIndex != -1:
                    clearName = obj.name[:dataIndex] + obj.name[dataEndIndex + 1:]
                    obj.name = clearName

                # Convert data to JSON string
                data_json = json.dumps(data)
                print(f"JSON Data: {data_json}")
                
                obj.name = obj.name + data_json

        else:
            print('NO_SELECTED_OBJECTS')
        
        return {'FINISHED'}

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

class COLLECTION_PT_RobloxPackagePanel(bpy.types.Panel):
    bl_label = "Roblox Package Panel"
    bl_idname = "COLLECTION_PT_roblox_package"
    bl_space_type = 'PROPERTIES'
    bl_region_type = 'WINDOW'
    bl_context = "collection"

    def draw(self, context):
        layout = self.layout

        # Botão para adicionar a propriedade de pacote
        row = layout.row()
        row.operator("object.package_property_operator", text="Add Package Property")

# Registrar classes
def register():
    bpy.utils.register_class(OBJECT_PT_RobloxMaterialPanel)
    bpy.utils.register_class(OBJECT_OT_ApplyRobloxMaterial)
    bpy.utils.register_class(OBJECT_OT_RemoveRobloxMaterial)
    bpy.utils.register_class(OBJECT_OT_ApplyData)
    bpy.utils.register_class(PackagePropertyOperator)
    bpy.utils.register_class(COLLECTION_PT_RobloxPackagePanel)
    bpy.types.Object.roblox_material_dropdown = bpy.props.EnumProperty(
        items=[
            ("Plastic", "Plastic", ""),
            ("Wood", "Wood", ""),
            ("Slate", "Slate", ""),
            ("Concrete", "Concrete", ""),
            ("CorrodedMetal", "Corroded Metal", ""),
            ("DiamondPlate", "Diamond Plate", ""),
            ("Foil", "Foil", ""),
            ("Grass", "Grass", ""),
            ("Ice", "Ice", ""),
            ("Marble", "Marble", ""),
            ("Granite", "Granite", ""),
            ("Brick", "Brick", ""),
            ("Pebble", "Pebble", ""),
            ("Sand", "Sand", ""),
            ("Fabric", "Fabric", ""),
            ("SmoothPlastic", "Smooth Plastic", ""),
            ("Metal", "Metal", ""),
            ("WoodPlanks", "Wood Planks", ""),
            ("Cobblestone", "Cobblestone", ""),
            ("Air", "Air", ""),
            ("Water", "Water", ""),
            ("Rock", "Rock", ""),
            ("Glacier", "Glacier", ""),
            ("Snow", "Snow", ""),
            ("Cement", "Cement", ""),
            ("Asphalt", "Asphalt", ""),
            ("LeafyGrass", "Leafy Grass", ""),
            ("Salt", "Salt", ""),
            ("Limestone", "Limestone", ""),
            ("Pavement", "Pavement", ""),
            ("Brickwork", "Brickwork", ""),
            ("Glow", "Glow", ""),
            ("Neon", "Neon", ""),
            ("Glass", "Glass", ""),
            ("Metallic", "Metallic", ""),
            ("Plaster", "Plaster", ""),
            ("Foam", "Foam", ""),
            ("SmoothMetal", "Smooth Metal", ""),
            ("WoodenPlanks", "Wooden Planks", ""),
            ("Cobble", "Cobble", ""),
            ("Diamond", "Diamond", ""),
            ("Sandstone", "Sandstone", ""),
            ("Pebblestone", "Pebblestone", ""),
            ("Custom", "Custom", "")
        ],
        name="Material Type"
    )

def unregister():
    bpy.utils.unregister_class(OBJECT_PT_RobloxMaterialPanel)
    bpy.utils.unregister_class(OBJECT_OT_ApplyRobloxMaterial)
    bpy.utils.unregister_class(OBJECT_OT_RemoveRobloxMaterial)
    bpy.utils.unregister_class(OBJECT_OT_ApplyData)
    bpy.utils.unregister_class(PackagePropertyOperator)
    bpy.utils.unregister_class(COLLECTION_PT_RobloxPackagePanel)
    del bpy.types.Object.roblox_material_dropdown

if __name__ == "__main__":
    register()

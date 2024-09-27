import bpy
import json
import math

print("########")

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

selected_objects = bpy.context.selected_objects

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
                material_name = material.name.split('_')[0]
                #data["M"] = material_name
                #print(f"Material name: {material_name}")
                
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
                data["M"] = None
                data["C"] = None
                print("First material slot is empty")
        else:
            data["M"] = None
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

from PIL import Image, ImageDraw, ImageColor
import numpy as np
import xml.etree.ElementTree as ET
import PIL.ImageDraw as ImageDraw
import PIL.Image as Image

def env_xml_maker(obstacle_list,region_arrays,region_tags,map_size,env_name):
    env =  ET.Element("environment")
    env.set("configfile","data/regiontypes.cfg")
    layer_0 = ET.SubElement(env, "layer")
    layer_0.set("id","0")
    geometry = ET.SubElement(layer_0,"geometry")
    geometry.set("border","true")
    regions= ET.SubElement(layer_0,"regions")
    walkable_area=ET.SubElement(geometry,"walkablearea")
    point2D = ET.SubElement(walkable_area,"point2d")
    point2D.set("x","0")
    point2D.set("y","0")

    point2D =  ET.SubElement(walkable_area,"point2d")
    point2D.set("x",f"{map_size[0]}")
    point2D.set("y","0")

    point2D = ET.SubElement(walkable_area,"point2d")
    point2D.set("x",f"{map_size[0]}")
    point2D.set("y",f"{map_size[1]}")
    
    point2D=ET.SubElement(walkable_area,"point2d")
    point2D.set("x","0")
    point2D.set("y",f"{map_size[1]}")
    for index, obstacle in enumerate(obstacle_list):
        obstacle_type="polygon"
        obstacle_entry = ET.SubElement(geometry,"obstacle")
        obstacle_entry.set("type",f"{obstacle_type}")
        for point in obstacle:
            point2D=ET.SubElement(obstacle_entry,f"point2d")
            point2D.set("x",f"{point[0]}")
            point2D.set("y",f"{point[1]}")
    for index, region in enumerate(region_arrays):
        region_entry = ET.SubElement(regions,"region")
        region_entry.set("type",f"{region_tags[index]}")
        for point in region:
            point2D=ET.SubElement(region_entry,f"point2d")
            point2D.set("x",f"{point[0]}")
            point2D.set("y",f"{point[1]}")
    xml_data = ET.tostring(env,encoding='utf8', method='xml').decode()

    file= open("Maps//NY.env","w")
    file.write(xml_data)
from PIL import Image, ImageDraw, ImageColor
import numpy as np
import xml.etree.ElementTree as ET
green_road_length=3170
width=2900


pixel_width=1500

block_width=282
block_height=73
street_width=15
street_pavement=4.5
avenue_width=21
avenue_pavement=5.5
n_blocks_hor=12
n_blocks_vert=39
scale=0.2412
variables=[block_width, block_height, street_width,avenue_width,avenue_pavement,street_pavement]
scaled_variables=[x*scale for x in variables]
block_width, block_height, street_width,avenue_width,avenue_pavement,street_pavement = scaled_variables

def middle_to_top_left(rect_array,map_width):
    return rect_array #- np.array([map_width,map_width])
def array_to_trash(rect_array,map_width):
    top_left=rect_array[1,:]
    bot_right=rect_array[3,:]
    list_trash=[top_left,bot_right]
    return [tuple(middle_to_top_left(x,map_width)) for x in list_trash]
def block(bot_left,block_width,block_height):
    assert bot_left.shape == (2,)
    ans= np.zeros(shape=(4,2))
    ans[0,:]=bot_left
    ans[1,:]=bot_left+np.array([0,block_height])
    ans[2,:]= ans[1,:] + np.array([block_width,0])
    ans[3,:]= ans[0,:] +np.array([block_width,0])
    return ans

map_width = (block_width+avenue_width+avenue_pavement)*n_blocks_hor + avenue_width+avenue_pavement
map_width= int(map_width) +1
if not  map_width % 2 == 0 :
    map_width+=1

corner=np.array([0,0]) #- np.array([map_width/2,map_width/2])


def corners_grid(start_corner,n_hor,n_vert,hor_dist,vert_dist):
    block_corners=[]
    for i in range(0,n_vert):
        for j in range(0,n_hor):
            block_corners.append(start_corner+np.array([hor_dist*j,vert_dist*i]))

    return block_corners

corners= corners_grid(corner,n_blocks_hor,n_blocks_vert,block_width+avenue_width+avenue_pavement*2,block_height+street_width+street_pavement*2)


def block_to_alley(block_array,alley_percent,alley_offset):
    top_left=block_array[1,:]
    top_right=block_array[2,:]
    bot_left=block_array[0,:]
    bot_right=block_array[3,:]
    block_width= np.linalg.norm(top_left-top_right)
    block_height=np.linalg.norm(top_left-bot_left)
    alley_width=int(alley_percent*block_width)
    alley_top_left=top_left+np.array([(block_width-alley_width)/2 + (block_width-alley_width)*alley_offset/2,0])
    alley_top_right=alley_top_left+np.array([alley_width,0])
    alley_bot_left= alley_top_left - np.array([0,block_height])
    alley_bot_right= alley_bot_left  + np.array([alley_width,0])
    alley_array=block(alley_bot_left,alley_width,block_height)
    block_left_width=np.linalg.norm(bot_left-alley_bot_left)
    block_left_array=block(bot_left,block_left_width,block_height)
    block_right_width=np.linalg.norm(alley_bot_right-bot_right)
    block_right_array=block(alley_bot_right+np.array([1,0]),block_right_width,block_height) #addition to not overlap

    return block_left_array, alley_array, block_right_array
    
    

img = Image.new("RGB", (map_width, map_width))
canvas = ImageDraw.Draw(img) 
polygon_list=[]

#obstacle loop
for corner in corners:
    red = np.random.randint(0,255)
    green = np.random.randint(0,255)
    blue =  np.random.randint(0,255)
    color=(red,green,blue) 
    color="green"

    block_array=block(corner,block_width,block_height)
    if np.random.randint(1,101)<0:
        alley_offset= np.random.normal(loc=0,scale=0.3)
        block_left_array, alley_array, block_right_array = block_to_alley(block_array,0.2,alley_offset)
        shape=array_to_trash(block_left_array,map_width)
        canvas.rectangle(shape, fill =color) 
        shape=array_to_trash(alley_array,map_width)
        canvas.rectangle(shape,fill="grey")
        shape=array_to_trash(block_right_array,map_width)
        canvas.rectangle(shape,fill=color)
        continue
    polygon_list.append(block_array)
   
    shape=array_to_trash(block_array,map_width)



    canvas.rectangle(shape, fill =color) 


#region loop
region_tags=[]
region_arrays=[]
for block_array in polygon_list:
    top_left=block_array[1,:]
    top_right=block_array[2,:]
    bot_left=block_array[0,:]
    bot_right=block_array[3,:]
    pavement_left=block(bot_left-np.array([avenue_pavement,0]),avenue_pavement,block_height)
    pavement_right=pavement_left + np.array([block_width+avenue_pavement,0])
    pavement_top=block(top_left,block_width,street_pavement)
    pavement_bot=pavement_top-np.array([0,block_height+street_pavement])
    region_arrays.append(pavement_left)
    region_arrays.append(pavement_right)
    region_arrays.append(pavement_top)
    region_arrays.append(pavement_bot)
    region_tags += ["sidewalk"]*4



for region in region_arrays:
    shape=array_to_trash(region,map_width)
    canvas.rectangle(shape,fill="grey")


img.show()


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
    

    

    # ET.dump(a)



    xml_data = ET.tostring(env,encoding='utf8', method='xml').decode()
    # xml_data=str(xml_data)
    file= open("NY.env","w")
    file.write(xml_data)

obstacle_list = polygon_list




#for test



env_xml_maker(obstacle_list,region_arrays,region_tags,[map_width,map_width],"NY")
print("done")
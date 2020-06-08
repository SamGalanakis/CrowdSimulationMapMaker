from PIL import Image, ImageDraw, ImageColor
import numpy as np
import xml.etree.ElementTree as ET
import PIL.ImageDraw as ImageDraw
import PIL.Image as Image
from helper import env_xml_maker
import copy
green_road_length=3170
width=2900
pixel_width=1500

block_width=282
block_height=73
street_width=15
street_pavement=4.5
n_hor=12
n_vert=2
avenue_width=21
avenue_pavement=5.5

scale=0.2412
scale=1
variables=[block_width, block_height, street_width,avenue_width,avenue_pavement,street_pavement]
scaled_variables=[x*scale for x in variables]
block_width, block_height, street_width,avenue_width,avenue_pavement,street_pavement = scaled_variables


def arr(x,y):
    return np.array([x,y])




def corner_to_array(bot_left,width,height):
    ans= np.zeros(shape=(4,2))
    ans[0,:]=bot_left
    ans[1,:]=bot_left+np.array([0,height])
    ans[2,:]= ans[1,:] + np.array([width,0])
    ans[3,:]= ans[0,:] +np.array([width,0])
    return ans

# so i is roads from bottom to top 
#j is avenue from left to right
def copy_grid(array,n_hor,n_vert,hor_dist,vert_dist):
    array_list=[]
    for i in range(0,n_vert):
        for j in range(0,n_hor):
            array_list.append(array+arr(hor_dist*j,vert_dist*i))
    return array_list

map_width = (block_width+avenue_width+avenue_pavement)*n_hor + avenue_width+avenue_pavement
map_width= int(map_width) +1
v_dist=block_height+street_width+street_pavement*2
h_dist=block_width+avenue_width+avenue_pavement*2

if not  map_width % 2 == 0 :
    map_width+=1

corner=arr(0,0)
# corner=arr(300,300)
block_0=corner_to_array(corner,block_width,block_height)

#pavements
pavement_top=corner_to_array(block_0[1,:],block_width,street_pavement)
pavement_bot=pavement_top-arr(0,block_height+street_pavement)
pavement_left=corner_to_array(corner+arr(-avenue_pavement,-street_pavement),avenue_pavement,block_height+2*street_pavement)
pavement_right=pavement_left+arr(block_width+avenue_pavement,0)

#crosses
top_left_cross=corner_to_array(corner+arr(-avenue_pavement,block_height+street_pavement),avenue_pavement,street_width)
top_right_cross=top_left_cross+arr(avenue_pavement+block_width,0)
# bot_left_cross=top_left_cross-arr(0,block_height+2*street_pavement+street_width)
# bot_right_cross=bot_left_cross+arr(avenue_pavement+block_width,0)

side_top_cross=corner_to_array(block_0[2,:]+arr(avenue_pavement,0),avenue_width,street_pavement)
side_bot_cross=side_top_cross-arr(0,block_height+street_pavement)



regions=[pavement_top,pavement_bot,pavement_left,pavement_right,top_left_cross,top_right_cross,side_top_cross,side_bot_cross]
region_tags=["pavement"]*4+["road marking"]*4


#road_obstacles

top_road=corner_to_array(block_0[1,:]+arr(0,street_pavement),block_width,street_width)
right_road=corner_to_array(corner+arr(block_width+avenue_pavement,0),avenue_width,block_height)
intersection_obstacle=corner_to_array(block_0[2,:]+arr(avenue_pavement,street_pavement),avenue_width,street_width)


obstacles=[block_0,top_road,right_road,intersection_obstacle]
obstacle_tags=["block","road_top","road_right","intersection"]
region_list=[]
obstacle_list=[]
region_tags_list=[]
n_hor=12
n_vert=39#39
# n_hor=n_vert=2
for index,region in enumerate(regions):
    
    region_list.extend(copy_grid(region,n_hor,n_vert,h_dist,v_dist))
    region_tags_list.extend([region_tags[index]]*(n_hor*n_vert))
for index,obstacle in enumerate(obstacles):
    obstacle_list.extend(copy_grid(obstacle,n_hor,n_vert,h_dist,v_dist))

def close_road(obstacle_list,road_index,n_hor,n_vert,region_list,regions_tags_list):

    
    for x in [1]:
        block_row_start=road_index*n_hor
        obstacle_start=n_hor*n_vert*x
        extracted=copy.deepcopy(obstacle_list[obstacle_start+block_row_start:obstacle_start+block_row_start+n_hor])
        del obstacle_list[obstacle_start+block_row_start:obstacle_start+block_row_start+n_hor]
        region_list.extend(extracted)
        regions_tags_list.extend(["grass"]*n_hor)
    return region_list,region_tags_list




# region_list,region_tags_list = close_road(obstacle_list,17,n_hor,n_vert,region_list,region_tags_list)
# region_list,region_tags_list = close_road(obstacle_list,17,n_hor,n_vert,region_list,region_tags_list)
env_xml_maker(obstacle_list,region_list,region_tags_list,[map_width,map_width],"NY")





print("Done")
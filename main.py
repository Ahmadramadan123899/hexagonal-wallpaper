from PIL import Image
import numpy as np

Input_filename="file.png"
def load_image(path):
    image=Image.open(path).convert("RGB")
    return np.array(image)

image_array=load_image(Input_filename)
height,width, _=image_array.shape
print(f"loaded image with dimensions:{width}x{height}")

import math 
def hex_grid_centers(width,height,hex_radius):
    centers=[]
    dx=3/2*hex_radius
    dy=math.sqrt(3)*hex_radius
    for row in range(int(height//dy)):
        for col in range(int(width//dx)):
            cx=col*dx
            cy=row*dy+(hex_radius*math.sqrt(3)/2 if col % 2 else 0)
            centers.append((int(cx),int(cy)))
    return centers

def sample_hex_color(image_array,cx,cy,r):
    pixels=[]
    for x in range(cx-r,cx+r):
        for y in range(cy-r,cy+r):
            if 0<= x < image_array.shape[1] and 0<=y<image_array.shape[0]:
                dx=x-cx
                dy=y-cy
                if abs(dx) + abs(dy)<r*1.5:
                    pixels.append(image_array[y,x])
        if pixels:
            return tuple(np.mean(pixels,axis=0).astype(int))
        return (0,0,0)
    
import svgwrite

def draw_hexagon(dwg,cx,cy,r,color):
    points=[]
    for i in range(6):
        angle=math.radians(60*i)
        x=cx+r*math.cos(angle)
        y=cy+r*math.sin(angle)
        points.append((x,y))
    hex =dwg.polygon(points,fill=svgwrite.rgb(*color))
    dwg.add(hex)

def generate_svg(image_array,hex_radius,output_file):
    height,width,_=image_array.shape
    dwg=svgwrite.Drawing(output_file,size=(width,height))
    centers=hex_grid_centers(width,height,hex_radius)
    for cx,cy in centers:
        color=sample_hex_color(image_array,cx,cy,hex_radius)
        draw_hexagon(dwg,cx,cy,hex_radius,color)
    dwg.save()

Output_filename="file.svg"
HEX_RADIUS=10
generate_svg(image_array,HEX_RADIUS,Output_filename)
print(f"SVG saved to {Output_filename}")
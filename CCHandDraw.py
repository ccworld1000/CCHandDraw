#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
#  CCHandDraw.py
#  
#  Created by CC on 2017/09/17.
#  Copyright 2017 youhua deng (deng you hua | CC) <ccworld1000@gmail.com>
#  https://github.com/ccworld1000/CCHandDraw
#  
#  This program is free software; you can redistribute it and/or modify
#  it under the terms of the GNU General Public License as published by
#  the Free Software Foundation; either version 2 of the License, or
#  (at your option) any later version.
#  
#  This program is distributed in the hope that it will be useful,
#  but WITHOUT ANY WARRANTY; without even the implied warranty of
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#  GNU General Public License for more details.
#  
#  You should have received a copy of the GNU General Public License
#  along with this program; if not, write to the Free Software
#  Foundation, Inc., 51 Franklin Street, Fifth Floor, Boston,
#  MA 02110-1301, USA.
#  
#  

#from PIL import Image 
from PIL import Image, ImageDraw, ImageFont
import numpy as np


  
# 指定要使用的字体和大小；/Library/Fonts/是macOS字体目录；Linux的字体目录是/usr/share/fonts/
font = ImageFont.truetype('/Library/Fonts/Arial.ttf', 24 * 5)
  
# image: 图片  text：要添加的文本 font：字体
def add_text_to_image(image, text, font=font):
  rgba_image = image.convert('RGBA')
  text_overlay = Image.new('RGBA', rgba_image.size, (255, 255, 255, 0))
  image_draw = ImageDraw.Draw(text_overlay)
  
  text_size_x, text_size_y = image_draw.textsize(text, font=font)
  # 设置文本文字位置
  print(rgba_image)
  text_xy = (rgba_image.size[0] - text_size_x, rgba_image.size[1] - text_size_y)
  # 设置文本颜色和透明度
  image_draw.text(text_xy, text, font=font, fill=(76, 234, 124, 180))
  
  image_with_text = Image.alpha_composite(rgba_image, text_overlay)
  
  return image_with_text
  
#im_before = Image.open("lena.jpg")
#im_before.show()
#im_after = add_text_to_image(im_before, 'WTF')
#im_after.show()
## im.save('im_after.jpg')


def handDraw (srcName, dstName) :
	asarray = np.asarray(Image.open(srcName).convert('L')).astype('float') 
	
	depth = 10. # (0-100) 
	
	grad = np.gradient(asarray) #取图像灰度的梯度值 
	gradient_x, gradient_y = grad #分别取横纵图像梯度值 
	gradient_x = gradient_x * depth /100. 
	gradient_y = gradient_y * depth /100. 
	
	sq = np.sqrt(gradient_x ** 2 + gradient_y ** 2 + 1.) 
	unit_x = gradient_x / sq 
	unit_y = gradient_y / sq 
	unit_z = 1. / sq 
	
	vec_el = np.pi/2.2 # 光源的俯视角度，弧度值 
	vec_az = np.pi/4. # 光源的方位角度，弧度值 
	
	dx = np.cos(vec_el)*np.cos(vec_az) #光源对x 轴的影响 
	dy = np.cos(vec_el)*np.sin(vec_az) #光源对y 轴的影响 
	dz = np.sin(vec_el) #光源对z 轴的影响 

	b = 255*(dx*unit_x + dy*unit_y + dz*unit_z) #光源归一化 
	b = b.clip(0,255) 

	saveImage (b, dstName)

def saveImage (b, dstName) :
	img = Image.fromarray(b.astype('uint8')) #重构图像 
	img.save(dstName) 
	
	#创建绘制对象  
	#draw = ImageDraw.Draw(img)
	
	#im_before.show()
	im_after = add_text_to_image(img, 'CC Camera')
	#im_after.save(dstName)
	#im_after.show()
	# im.save('im_after.jpg')
	im_after.save(dstName+'.png')
	
	#draw.text((100, 50), u'CC Camera', 'fuchsia', font) 
	#img.save(dstName+'.png')
	
	#im_before = Image.open(dstName)
	##im_before.show()
	#im_after = add_text_to_image(im_before, 'CC Camera')
	##im_after.save(dstName)
	##im_after.show()
## im.save('im_after.jpg')
	#im_after.save(dstName+'.png')

	print(dstName)

def main(args):
    return 0

if __name__ == '__main__':
    import sys
    sys.exit(main(sys.argv))

#!/bin/python
import os, sys
from PIL import Image

class resize_image():
		'''  This class will take an image and resize it to the width requested
				 if the width is greater than the width provided '''
		def __init__(self):
				pass
		
		def find_files(self):
				matches = []
				rootDir = '/www/sites/sjdsdirectory/media/business_images/'
				i = 0 # directory count
				j = 0 # file count
				for dirName, subdirList, fileList in os.walk(rootDir):
						if dirName.find('.git') < 0:
								i = i+1
								for fname in fileList:
										im = Image.open(dirName + '/' + fname)
										im_size = im.size
										if im_size[0] > 1000:
												width_ratio = 1000/float(im_size[0])
												new_height = int(width_ratio * im_size[1])
												filesize_bytes = os.path.getsize(dirName + '/' + fname)
												filesize_kb = filesize_bytes / 1024
												print dirName, fname, " Orig size %s" % filesize_kb
												im.resize((1000, new_height), Image.ANTIALIAS).save(dirName + '/' + fname)
												filesize_bytes = os.path.getsize(dirName + '/' + fname)
												filesize_kb = filesize_bytes / 1024
												print dirName, fname, " Resized to %s" % filesize_kb
if __name__ == "__main__":
		rs = resize_image()
		rs.find_files()
		print "Done"



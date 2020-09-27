from pywinauto.application import Application
from PIL import Image, ImageChops


class ImageViewer(object):
	class CaptureError(Exception):pass
	def connect(self, path):
		return Application(backend='uia').connect(path=path)

	@staticmethod
	def trim(im):
		bg = Image.new(im.mode, im.size, im.getpixel((0,0)))
		diff = ImageChops.difference(im, bg)
		diff = ImageChops.add(diff, diff, 2.0, -100)
		bbox = diff.getbbox()
		if bbox:return im.crop(bbox)

	def stream(self):
		cache = None
		while 1:
			try:
				img = self.window.capture_as_image()
			except Exception as e:
				raise self.CaptureError(e)
			if cache==img:continue
			cache = img
			img = self.trim(img)
			yield img


class NoMacs(ImageViewer):
	def __init__(self, path=r"nomacs.exe"):
		app = self.connect(path)
		window = app.top_window()
		self.window = window.child_window(class_name="nmc::DkViewPort")

class XnView(ImageViewer):
	def __init__(self, path=r'xnviewmp.exe'):
		app = self.connect(path)
		window = app.top_window()
		self.window = window.child_window(class_name="MyBitmapView")

if __name__ == '__main__':
	import dlib
	import numpy as np
	
	# viewer = NoMacs()
	viewer = XnView()

	win = dlib.image_window()
	for img in viewer.stream():
		img = np.array(img)
		win.set_image(img)
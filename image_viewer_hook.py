from pywinauto.application import Application
import numpy as np

from PIL import Image, ImageChops

class ImageViewer(object):
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
			img = self.window.capture_as_image()
			if cache==img:continue
			cache = img
			img = self.trim(img)
			img = np.array(img)
			yield img

class XnView(ImageViewer):
	def __init__(self, path=XNVIEW_PATH):
		app = self.connect(path)		# window = app.top_window()
		window = self.app.window(class_name='Qt5QWindowIcon')
		window = window.Custom.Pane.Custom
		self.window = window.Custom

class NoMacs(ImageViewer):
	def __init__(self, path=NOMACS_PATH):
		app = self.connect(path)
		window = app.top_window()
		self.window = window.child_window(auto_id="DkNoMacs.DkCentralWidget", control_type="Custom")

if __name__ == '__main__':
	import dlib
	# viewer = XnView()
	viewer = NoMacs()
	win = dlib.image_window()
	for img in viewer.stream():
		win.set_image(img)
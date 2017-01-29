#!/usr/bin/python
import PIL.Image, PIL.ExifTags, glob, os, time, logging, sys

def deco(cls):
	cls.set_properties()
	return cls

@deco
class Photo(object):
	'''
	'''
	FILETYPES = ('.jpg', '.jpeg', '.png', '.tif', '.tiff', '.gif', '.xcf')
	RAWTYPES = ('.NEF', '.nef')

	@classmethod
	def set_properties(cls):
		'''
		Dynamically set class properties.
		'''
		for item in PIL.ExifTags.TAGS.values():
			setattr(cls, item, cls.exif_property(item))

	@classmethod
	def exif_property(cls, exif_property_name, docstring=None):
		'''
		Exif Factory Function. For a given property name returns property object.
		
		'''
		def getter(self):
			try:
			    return self._exif[exif_property_name]
			except KeyError:
			    return None
		return property(getter, doc=docstring)

	def __init__(self, filename):
		super(Photo, self).__init__()
		if not os.path.isfile(filename):
			raise PhotoException('Error: {0} - no such file'.format(filename))

		if not filename.lower().endswith(self.FILETYPES):
			raise PhotoException('Error: {0} - not a valid extension'.format(filename))

		path, self.__suffix = os.path.splitext(filename)
		self.__basename = os.path.basename(path)
		self.__dirname = os.path.dirname(path)
		self.__size = os.path.getsize(filename)
		self._exif = self.__get_exif()
		self.__rawtype = self.__hasRAW()

	@property
	def basename(self):
		return self.__basename

	@property
	def dirname(self):
		return self.__dirname

	@property
	def suffix(self):
		return self.__suffix

	@property
	def rawtype(self):
		return self.__rawtype

	@property
	def size(self):
		return self.__size

	@property
	def file(self):
		return ''.join([self.basename, self.suffix])

	@property
	def filename(self):
		return os.path.abspath(os.path.join(self.dirname, self.file))

	@property
	def rawfile(self):
		return ''.join([self.basename, self.rawtype]) if self.rawtype else None

	def __rename(self, destination, basename):
		'''
		'''
		if self.basename != basename:
			logging.warning('Renaming %s -> %s', self.basename, basename)
			self.__basename = basename
		self.__dirname = os.path.abspath(destination)

	def __get_exif(self):
		'''
		'''
		try:
			with PIL.Image.open(self.filename) as img:
				exif = { PIL.ExifTags.TAGS[k]: v for k, v in img._getexif().items() if k in PIL.ExifTags.TAGS }
		except IOError as e:
			raise PhotoException(str(e))
		return exif

	def __hasRAW(self):
		'''
		'''
		for rawtype in Photo.RAWTYPES:
			raw_file =  os.path.join(self.dirname, ''.join([self.basename, rawtype]))
			if os.path.isfile(raw_file):
				return rawtype

		return None

	def move_file(self, destination, dryrun=False, rename=False):
		'''
		'''
		if not os.path.exists(destination):
			if not dryrun:
				os.makedirs(destination, 0755)
			logging.info('%s created', destination)

		src_file, src_dirname, src_rawfile = self.file, self.dirname, self.rawfile

		if rename:
			from random import randint
			basename = '{0}-{1}'.format(self.basename, str(randint(1000, 9999)))
		else:
			basename = self.basename
		
		self.__rename(destination, basename)

		try:
			src, dst  = os.path.join(src_dirname, src_file), self.filename
			if not dryrun: 
				os.rename(src, dst)
			logging.info('%s -> %s', src, dst)

			if src_rawfile:
				src, dst = os.path.join(src_dirname, src_rawfile), os.path.join(self.dirname, self.rawfile)
				if not dryrun:
					os.rename(src, dst)
				logging.info('%s -> %s', src, dst)

		except OSError as err:
			logging.error('Error: %s: Unable to rename file %s', str(err), src)

class PhotoException(Exception):
	'''
	'''
	pass

def get_files(directory, extensions):
	'''
	'''
	if not os.path.isdir(directory):
		logging.error('Error: %s is not directory', str(directory))
		os.exit(1)

	filenames = set()
	for root, directorys, files in os.walk(directory):
		for file in files:
			path = os.path.abspath(os.path.join(root, file))
			if path.lower().endswith(extensions):
				filenames.add(path)

	return filenames

def main():
	old_dir = '/media/ntfs-share/Data/Pictures/Nikon'
	new_dir = '/media/ntfs-share/Data/Pictures/nikon'
	dryrun = False
	mapping = {}
	logfile = os.path.join(old_dir,'exifsort.log')
	logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
		filename=logfile,level=logging.DEBUG)

	print 'Creating file mappings. Check log file {0} for more details'.format(logfile)
	
	for item in get_files(old_dir, Photo.FILETYPES):
		item = Photo(item)
		if item.DateTimeOriginal:
			date = item.DateTimeOriginal.split()[0]
		elif item.DateTime:
			date = item.DateTime.split()[0]
		elif item.DateTimeDigitized:
			date = item.DateTimeDigitized.split()[0]
		else:
			logging.info('SKIPPING - no suitable date for %s!', item.filename)
			continue

		year, month, day = date.split(':')

		if item.basename in mapping:
			if item.size == mapping[item.basename]:
				logging.warning('%s file with a same name (%s) and size (%s) already exists!', 
					item.filename, item.file, item.size)
			else:
				logging.warning('%s file with a same name (%s) but different size (%s/%s) already exists!', 
					item.filename, item.file, item.size, mapping[item.basename])
			item.move_file(os.path.join(new_dir, year, month, day), dryrun=dryrun, rename=True)
			continue

		mapping[item.basename] = item.size
		item.move_file(os.path.join(new_dir, year, month, day), dryrun=dryrun, rename=False)

if __name__=='__main__': main()
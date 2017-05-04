#!/usr/bin/python3

import struct

class StructField:
	'''
	Descriptor representing a simple structure field.
	'''
	def __init__(self, fmt, offset):
		self.format = fmt
		self.offset = offset

	def __get__(self, instance, cls):
		if instance is None:
			return self
		else:
			r = struct.unpack_from(self.format, instance._buffer, self.offset)
			return r[0] if len(r) == 1 else r

class StructureMeta(type):
	'''
	Metaclass that automatically creates StructField descriptor.
	'''
	def __init__(self, clsname, bases, clsdict):
		fields = getattr(self,  '_fields_', [])
		byte_order = ''
		offset = 0
		for fmt, fieldname in fields:
			if fmt.startswith(('<', '>', '!', '@')):
				byte_order = fmt[0]
				fmt = fmt[1:]
			fmt = byte_order + fmt
			setattr(self, fieldname, StructField(fmt, offset))
			offset += struct.calcsize(fmt)
		setattr(self, 'struct_size', offset)


class Structure(metaclass=StructureMeta):
	'''
	Base class that accepts some byte data and stores it as the underlying memory buffer.
	'''
	def __init__(self, bytedata):
		self._buffer = memoryview(bytedata)

	@classmethod
	def from_file(cls, f):
		return cls(f.read(cls.struct_size))


class PolyHeader(Structure):
	_fields_ = [
		('<i', 'file_code'),
		('d', 'min_x'),
		('d', 'min_y'),
		('d', 'max_x'),
		('d', 'max_y'),
		('i', 'num_polys')
	]
#!/usr/bin/env python3

class Person(object):

    def addProperty(self, attribute):
        # create local setter and getter with a particular attribute name 
        getter = lambda self: self._getProperty(attribute)
        setter = lambda self, value: self._setProperty(attribute, value)

        # construct property attribute and add it to the class
        setattr(self.__class__,
                attribute,
                property(fget=getter, fset=setter, doc="Auto-generated method")
                )

    def _setProperty(self, attribute, value):
        print("Setting: %s = %s" %(attribute, value))
        setattr(self, '_' + attribute, value.title())    

    def _getProperty(self, attribute):
        print("Getting: %s" %attribute)
        return getattr(self, '_' + attribute)

if __name__ = '__main__':
    user = Person()
    user.addProperty('name')
    user.addProperty('phone')

    user.name = 'john smith'
    user.phone = '12345'

    user.name
    user.__dict__
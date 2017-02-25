#!/usr/bin/env python3

import functools
import inspect
from itertools import chain

def annotation_decorator(process):
  '''
  Creates a decorator that process annotations for each argument passed
  into its target function, raising an exception if there's a problem.
  '''

  def annotator(*args, **kwargs):
    annotations = kwargs.copy()

    @functools.wraps(process)
    def decorator(func):
      spec = inspect.getfullargspec(func)
      annotations.update(zip(spec.args, args))
  
        defaults = spec.defaults or ()
        defaults_zip = zip(spec.args[-len(defaults):], defaults)
        kwonlydefaults = spec.kwonlydefaults or {}
  
        for name, value in chain(defaults_zip, kwonlydefaults.items()):
          if name in annotations:
            process(value, annotations[name])
  
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
          new_args = []
          new_kwargs = {}
          keyword_args = kwargs.copy()
  
          # Deal with explicit arguments passed positionally
          for name, arg in zip(spec.args, args):
            if name in annotations:
              new_args.append(process(arg, annotations[name]))
  
          # Deal with explicit arguments passed by keyword
          for name in chain(spec.args, spec.kwonlyargs):
            if name in kwargs and name in annotations:
              new_kwargs[name] = process(keyword_args.pop(name),
                                        annotations[name])
  
          # Deal with variable positional arguments
          if spec.varargs and spec.varargs in annotations:
            annotation = annotations[spec.varargs]
            for arg in args[len(spec.args):]:
              new_args.append(process(arg, annotation))
  
          # Deal with variable keyword arguments
          if spec.varkw and spec.varkw in annotations:
            annotation = annotations[spec.varkw]
            for name, arg in keyword_args.items():
              new_kwargs[name] = process(arg, annotation)
  
          r = func(*new_args, **new_kwargs)
          if 'return' in annotations:
            r = process(r, annotations['return'])
          return r

        def return_annotator(annotation):
          annotations['return'] = annotation
        wrapper.returns = return_annotator

        return wrapper
  
    return decorator

  return annotator


@annotation_decorator
def typesafe(value, annotation):
  '''
  Verify that the function is called with the right argument types and
  that it returns a value of the right type, according to its annotations
  '''

  if not isinstance(value, annotation):
    raise TypeError('Expected %s, got %s.'% (annotation.__name__,
                                            type(value).__name__))

  return value

@annotation_decorator
def coerce_arguments(value, annotation):
  return annotation(value)
#!/usr/bin/env python
# -*- coding: utf-8 -*-


def time_recorder(func):
   def func_wrapper(*args, **kwargs):
       func_name = func.__name__
       print('[START - {0}]'.format(func_name))
       timer_start = datetime.datetime.now()
       ret = func(*args, **kwargs)
       timer_end = datetime.datetime.now()
       print('[END   - {0}] {1}'.format(func_name, timer_end - timer_start))
       return ret
   return func_wrapper



# @time_recorder

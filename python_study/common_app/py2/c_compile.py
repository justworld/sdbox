# coding: utf-8
"""
分析python字节码
"""
import dis

source = open('c_compile_test.py').read()
co = compile(source, 'c_compile_test.py', 'exec')
print('const : ', co.co_consts)
print('name : ', co.co_names)
dis.dis(co)

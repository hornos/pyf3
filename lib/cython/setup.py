from distutils.core import setup
from distutils.extension import Extension
from Cython.Distutils import build_ext

ext_modules = [Extension("math", ["math.pyx"],libraries=["m"])]

setup(
  name = 'Math lib',
  cmdclass = {'build_ext': build_ext},
  ext_modules = ext_modules
)

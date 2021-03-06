
from setuptools import setup

setup(name='tensor-layer-db',
      version='0.1',
      description='the model life cycle managment system',
      url='https://github.com/fangde/TensorLab',
      author='Fangde Liu',
      author_email='liufangde@surgicalai.cn',
      license='MIT',
      packages=['tensorlab'],
      install_requires=['pymongo','lz4','graphene','pyyaml'],
      zip_safe=False)
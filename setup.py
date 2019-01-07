from setuptools import setup

setup(
    name='ambient_aprs',
    version='0.10.0',
    packages=['ambient_aprs'],
    url='https://github.com/avryhof/ambient_aprs',
    license='MIT',
    author='Amos Vryhof',
    author_email='amos@vryhofresearch.com',
    description='A Python class for sending Ambient Weather API Data as APRS packets.',
    classifiers=[
          'Development Status :: 5 - Production/Stable',
          'Intended Audience :: Developers',
          'License :: OSI Approved :: MIT License',
          'Programming Language :: Python :: 3'
      ],
    install_requires=[
        "ambient-api",
    ],
)

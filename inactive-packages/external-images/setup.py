from setuptools import setup

setup(
    name='lektor-external-images',
    version='0.1',
    author=u'Odin H\xf8rthe Omdal',
    author_email='odin.omdal@gmail.com',
    license='MIT',
    py_modules=['lektor_external_images'],
    entry_points={
        'lektor.plugins': [
            'external-images = lektor_external_images:ExternalImagesPlugin',
        ]
    }
)

from setuptools import setup

setup(name='django-rest-captcha',
      version='0.1.1',
      description='Lightweight version of django-simple-captcha for work with django-rest-framework',
      url='https://github.com/lexaf/django-rest-captcha',
      author='evgeny.zuev <zueves@gmail.com>',
      author_email='zueves@gmail.com',
      license='MIT',
      packages=['rest_captcha'],
      install_requires=[
          'djangorestframework=^3.5',
          'django',
          'Pillow=^4.1.1'
      ],
      zip_safe=False)

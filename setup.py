from setuptools import setup, find_packages

setup(
    name='django-file-picker',
    version='0.8.2',
    author='Caktus Consulting Group and Evan Culver',
    author_email='solutions@caktusgroup.com',
    packages=find_packages(exclude=['sample_project']),
    include_package_data=True,
    #url='https://github.com/caktus/django-file-picker/',
    url='http://django-file-picker.readthedocs.org/',
    license='BSD',
    description='Pluggable file picker',
    classifiers=[
        'Topic :: Internet :: WWW/HTTP :: Dynamic Content',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: BSD License',
        'Programming Language :: Python',
        'Topic :: Software Development :: Libraries :: Python Modules',
        'Development Status :: 4 - Beta',
        'Operating System :: OS Independent',
    ],
    long_description=open('README.rst').read(),
    install_requires=['sorl-thumbnail==11.09','PIL==1.1.7', 'South==0.7.3', 'Embedly==0.4.3'],
    zip_safe=False, # because we're including media that Django needs
)


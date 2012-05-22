# -*- coding:utf-8 -*-

from setuptools import setup, find_packages
import os

version = '1.0a2.dev0'
long_description = open("README.txt").read() + "\n" + \
                   open(os.path.join("docs", "INSTALL.txt")).read() + "\n" + \
                   open(os.path.join("docs", "CREDITS.txt")).read() + "\n" + \
                   open(os.path.join("docs", "HISTORY.txt")).read()

setup(name='s17.tinymce.mediaembed',
      version=version,
      description="Media Embed plugin for TinyMCE",
      long_description=long_description,
      classifiers=[
        "Development Status :: 4 - Beta",
        "Environment :: Web Environment",
        "Framework :: Plone",
        "Framework :: Plone :: 4.1",
        "Framework :: Plone :: 4.2",
        "Intended Audience :: End Users/Desktop",
        "License :: OSI Approved :: GNU General Public License (GPL)",
        "Operating System :: OS Independent",
        "Programming Language :: JavaScript",
        "Programming Language :: Python",
        "Programming Language :: Python :: 2.6",
        "Topic :: Software Development :: Libraries :: Python Modules",
        ],
      keywords='plone audio video multimedia plugin tinymce',
      author='Silvestre Huens',
      author_email='s.huens@gmail.com',
      url='https://github.com/simplesconsultoria/s17.tinymce.mediaembed',
      license='GPL',
      packages=find_packages(exclude=['ez_setup']),
      namespace_packages=['s17', 's17.tinymce'],
      include_package_data=True,
      zip_safe=False,
      install_requires=[
        'setuptools',
        'five.grok>=1.2',
        's17.media.views',
        ],
      extras_require={
        'test': ['plone.app.testing'],
        },
      entry_points="""
      [z3c.autoinclude.plugin]
      target = plone
      """,
      )

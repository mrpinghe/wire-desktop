#!/usr/bin/python
# coding: utf-8

#
# Wire
# Copyright (C) 2016 Wire Swiss GmbH
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program. If not, see http://www.gnu.org/licenses/.
#

import os
import re
import sys

os.system('crowdin-cli --identity=keys/crowdin.yaml upload sources')
os.system('crowdin-cli --identity=keys/crowdin.yaml download')

os.chdir(os.path.dirname(os.path.realpath(__file__)))
root = 'electron/locale/'


def get_locale(filename):
  locale = filename.replace('strings-', '').replace('.js', '')
  return locale if len(locale) == 2 else None


for filename in os.listdir(root):
  locale = get_locale(filename)
  if locale:
    if locale not in ['de', 'ru']:
      file_to_delete = os.path.join(root, filename)
      print('Removing unsupported locale "%s" (%s)' % (locale, file_to_delete))
      os.remove(file_to_delete)
      continue

    with open(os.path.join(root, filename), 'r') as f:
      source = f.read()

    with open(os.path.join(root, filename), 'w') as f:
      source = source.replace('=', ' = ')
      source = source.replace("'use = strict';\n\n", '')
      source = re.sub(r'#(.)+\n', '', source)

      f.write("'use strict';\n\nlet string = {};\n\n")
      f.write(source)
      f.write('module.exports = string;\n')

  if filename == 'strings.js':
    with open(os.path.join(root, filename), 'r') as f:
      source = f.read()

    with open(os.path.join(root, filename.replace('.js', '-en.js')), 'w') as f:
      f.write("'use strict';\n\nlet string = {};\n\n")
      f.write(source.replace("'use strict';\n\n", ''))
      f.write('\nmodule.exports = string;\n')

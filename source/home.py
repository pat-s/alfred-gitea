#!/usr/bin/env python3
# encoding: utf-8
from workflow import Workflow3

wf = Workflow3(update_settings={
  'github_slug': 'pat-s/alfred-gitea',
})
url = wf.settings.get('base_url')
print(url)

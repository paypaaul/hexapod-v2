import os
import sys
from playwright.sync_api import sync_playwright as s
p = s().start(); b = p.chromium.launch(channel='chrome')
for nome in sys.argv[1:]:
    g = b.new_page(device_scale_factor=3, viewport={'width': 720, 'height': 500})
    g.goto('file://' + os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), nome + '.svg'))
    g.screenshot(path=os.path.join(os.environ.get('TMPDIR', '/tmp'), nome + '.png'), full_page=True, timeout=60000)
    g.close()
b.close(); p.stop()

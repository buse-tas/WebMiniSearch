import sys
sys.path.insert(1, '/home/u083/public_html/WebMiniSearch')

import os
os.chdir('/home/u083/public_html/WebMiniSearch')



from search_engine import app
application = app
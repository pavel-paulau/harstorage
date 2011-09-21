import logging

import os
import cairo
import rsvg
import hashlib
import Image
import shutil

from pylons import request, response
from pylons import config
from harstorage.lib.base import BaseController

log = logging.getLogger(__name__)

class ChartController(BaseController):
    def export(self):
        # Parameters
        type        = request.POST['type']
        svg         = request.POST['svg']
        filename    = request.POST['filename']
        width       = int( request.POST['width'] )
        
        # Sizes
        if width == 960:
            height = 400
        elif width == 450:
            height = 350
        elif width == 930:
            height = 550

        # Converting
        if type == 'image/png':
            # Filename
            ext         = '.png'
            img_name    = os.path.join( config['app_conf']['temp_store'], hashlib.md5().hexdigest() + ext )
            
            # Create PNG file
            self.render_png(svg,img_name,width,height)
        elif type == 'image/svg+xml':
            # Filename
            ext         = '.svg'
            img_name    = os.path.join( config['app_conf']['temp_store'], hashlib.md5().hexdigest() + ext )
            
            # Create SVG file
            self.render_svg(svg,img_name)
        
        # Response headers
        response.headers['Content-Disposition'] = "attachment; filename=" + filename + ext
        response.headers['Content-type']        = type
        
        # Response content        
        with open(tempname, 'rn') as f:
            shutil.copyfileobj(f, response)
        
    def render_svg(self,svg,filename):
        # Render SVG
        svg_file = open( filename,'w')
        svg_file.write( svg )
        svg_file.close()
        
    def render_png(self,svg,filename,width,height):
        # Create PNG image
        img = cairo.ImageSurface(cairo.FORMAT_ARGB32, width, height)
        ctx = cairo.Context(img)

        rsvg.Handle(None, svg).render_cairo(ctx)

        img.write_to_png(filename)
        
    def resize(self,filename,width, height):
        # Resize image
        im1 = Image.open(filename)
        image = im1.resize((width, height), Image.ANTIALIAS)
        image.save(filename)
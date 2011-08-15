import logging

import os
import cairo
import rsvg
import hashlib
import Image

from pylons import request, response, session, tmpl_context as c, url
from pylons import config
from pylons.controllers.util import abort, redirect

from harstorage.lib.base import BaseController, render
from harstorage.lib import helpers as h

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

        # File type
        response.headers['Content-type'] = type

        # Converting
        if type == 'image/png':
            # Filename
            ext         = '.png'
            tempname    = os.path.join( config['app_conf']['temp_store'], hashlib.md5().hexdigest() + ext )
            
            # Create PNG file
            self.render_png(svg,tempname,width,height)                                    
        elif type == 'image/svg+xml':
            # Filename
            ext         = '.svg'
            tempname    = os.path.join( config['app_conf']['temp_store'], hashlib.md5().hexdigest() + ext )
            
            # Create SVG file
            self.render_svg(svg,tempname)
        
        # Response headers
        file_size = os.path.getsize(tempname)            
        response.headers['Content-Disposition'] = "attachment; filename=" + filename + ext
        response.headers['Content-Length']      = str(file_size)
            
        # Response content
        f = open(tempname)        
        response.write(f.read())
        f.close()
        
    def render_svg(self,svg,filename):
        # Render SVG
        svg_file = open( filename,'w')
        svg_file.write( svg )
        svg_file.close()
        
    def render_png(self,svg,filename,width,height):
        # Create PNG image
        img =  cairo.ImageSurface(cairo.FORMAT_ARGB32, width, height)
        ctx = cairo.Context(img)

        rsvg.Handle(None, svg).render_cairo(ctx)

        img.write_to_png(filename)
        
    def resize(self,filename,width, height):
        # Resize image
        im1 = Image.open(filename)
        image = im1.resize((width, height), Image.ANTIALIAS)
        image.save(filename)
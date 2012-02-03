import logging
import os
import cairo
import rsvg
import hashlib

from pylons import request, response
from pylons import config
from pylons.decorators.rest import restrict

from harstorage.lib.base import BaseController

log = logging.getLogger(__name__)

class ChartController(BaseController):

    """
    Export charts in SVG and PNG format
    """

    @restrict('POST')
    def export(self):
        """Main export controller"""

        # Parameters from POST request
        type = request.POST['type']
        svg = request.POST['svg']
        filename = request.POST['filename']
        width = int( request.POST['width'] )

        # Image size
        if width == 960:
            height = 400
        elif width == 450 or width == 930:
            height = 300

        # Converting
        if type == 'image/png':
            # Image extension
            ext = '.png'

            # Image name
            image_name = os.path.join(config['app_conf']['temp_store'],
                                      hashlib.md5().hexdigest() + ext)
            
            # Create PNG file
            self._render_png(svg, image_name, width, height)
        elif type == 'image/svg+xml':
            # Image extension
            ext = '.svg'

            # Image name
            image_name = os.path.join(config['app_conf']['temp_store'],
                                      hashlib.md5().hexdigest() + ext)
            
            # Create SVG file
            self._render_svg(svg, image_name)
        
        # Response headers
        response.headers['Content-Disposition'] = "attachment; filename=" + filename + ext
        response.headers['Content-type'] = type
        
        # Return chuncked response
        return self._stream_image(image_name)
        
    def _render_svg(self, svg, filename):
        """Create SVG file"""
        
        with open(filename, 'w') as svg_file:
            svg_file.write(svg)
        
    def _render_png(self, svg, filename, width, height):
        """Create PNG file"""

        image = cairo.ImageSurface(cairo.FORMAT_ARGB32, width, height)
        ctx = cairo.Context(image)

        rsvg.Handle(None, svg).render_cairo(ctx)

        image.write_to_png(filename)

    def _stream_image(self, image_name):
        """Stream image by chunks"""

        with open(image_name, 'rb') as image_file:
            chunk = image_file.read(1024)
            while chunk:
                yield chunk
                chunk = image_file.read(1024)
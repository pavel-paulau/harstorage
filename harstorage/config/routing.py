from routes import Mapper

def make_map(config):
    """Create, configure and return the routes Mapper"""

    map = Mapper(directory=config['pylons.paths']['controllers'],
                 always_scan=config['debug'])
    map.minimization = False
    map.explicit = True

    # The ErrorController route (handles 4xx/5xx error pages)
    map.connect('/error/{action}', controller='error')

    # Home page
    map.connect('/', controller='results', action='index')

    # Common routing to controllers
    map.connect('/{controller}/{action}')

    return map
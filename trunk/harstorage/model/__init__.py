"""The application's model objects"""
from sqlalchemy import schema, types, orm
import sqlalchemy

from sqlalchemy.dialects.mysql import MEDIUMINT,INTEGER,VARCHAR,CHAR,TINYINT,TIMESTAMP
   
from harstorage.model import meta
#from harstorage.model.meta import Session, metadata
   
def init_model(engine):
    """Call me before using any of the tables or classes in the model"""
    sm = orm.sessionmaker(bind = engine, autoflush=True, expire_on_commit=True)
    meta.engine = engine
    meta.Session = orm.scoped_session(sm)
    meta.Session.configure(bind=engine)


urls_table = schema.Table('urls',meta.metadata,
    schema.Column('id',MEDIUMINT,primary_key=True),
    schema.Column('url',VARCHAR(255)),
    schema.Column('label',VARCHAR(255)),
    schema.Column('last_metric',INTEGER),
)
    
hars_table = schema.Table('hars',meta.metadata,
    schema.Column('id',INTEGER,primary_key=True),
    schema.Column('mongo_key',VARCHAR(24)),
    schema.Column('requests',MEDIUMINT),
    schema.Column('total_size',MEDIUMINT),
    schema.Column('html_size',MEDIUMINT),   
    schema.Column('js_size',MEDIUMINT),
    schema.Column('css_size',MEDIUMINT),
    schema.Column('image_size',MEDIUMINT),
    schema.Column('other_size',MEDIUMINT),
    schema.Column('full_time',MEDIUMINT),
)

metrics_table = schema.Table('metrics',meta.metadata,
    schema.Column('id',INTEGER,primary_key=True),
    schema.Column('url_id',INTEGER),
    schema.Column('har_id',INTEGER),
    schema.Column('pagespeed_id',INTEGER),
    schema.Column('timestamp',TIMESTAMP),
)

pagespeed_table = schema.Table('pagespeed',meta.metadata,
    schema.Column('id',INTEGER,primary_key=True),
    schema.Column('score',TINYINT),
)
   
class Urls(object):
    pass

class Hars(object):
    pass

class Metrics(object):
    pass

class PageSpeed(object):
    pass


orm.mapper(Urls,urls_table)
orm.mapper(Hars,hars_table)
orm.mapper(Metrics,metrics_table)
orm.mapper(PageSpeed,pagespeed_table)
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

urls_table = schema.Table('URLS',meta.metadata,
    schema.Column('id',MEDIUMINT,primary_key=True),
    schema.Column('url',VARCHAR(255)),
)

labels_table = schema.Table('LABELS',meta.metadata,
    schema.Column('id',MEDIUMINT,primary_key=True),
    schema.Column('label',VARCHAR(255)),
    schema.Column('last_metric',INTEGER),
)

testresults_table = schema.Table('TESTRESULTS',meta.metadata,
    schema.Column('id',INTEGER,primary_key=True),
    schema.Column('timestamp',TIMESTAMP),
    schema.Column('url_id',INTEGER),
    schema.Column('label_id',INTEGER),
    schema.Column('pagespeed_id',INTEGER),
    schema.Column('requests',MEDIUMINT),
    schema.Column('size',MEDIUMINT),
    schema.Column('time',MEDIUMINT),
    schema.Column('har_key',CHAR(24)),
    )

pagespeed_table = schema.Table('PAGESPEED',meta.metadata,
    schema.Column('id',INTEGER,primary_key=True),
    schema.Column('score',TINYINT),
)
   
class Urls(object):
    pass

class Labels(object):
    pass

class TestResults(object):
    pass

class PageSpeed(object):
    pass


orm.mapper(Urls,urls_table)
orm.mapper(Labels,labels_table)
orm.mapper(TestResults,testresults_table)
orm.mapper(PageSpeed,pagespeed_table)

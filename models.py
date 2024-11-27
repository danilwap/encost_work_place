from sqlalchemy import Column, Integer, String, JSON, Boolean

from database import Base, metadata

class Operators(Base):
    __table__ = metadata.tables["parameters.client_persons"]

class Endpoint(Base):
    __table__ = metadata.tables["spider.endpoints"]

class EndpointFlags(Base):
    __table__ = metadata.tables["parameters.endpoint_flags"]

class EndpointWeights(Base):
    __table__ = metadata.tables["parameters.endpoint_weights"]

class EndpointStates(Base):
    __table__ = metadata.tables["parameters.endpoint_states"]

class EndpointReasons(Base):
    __tablename__ = 'endpoint_reasons'

    id = Column(Integer, primary_key=True)
    client_id = Column(Integer)
    endpoint_id = Column(Integer)
    reason_type = Column(String(30))
    name = Column(String(100))
    hierarchy = Column(JSON)
    category = Column(String(30))
    actions = Column(JSON, nullable=False, default='[]')
    is_fixed = Column(Boolean)
    color = Column(String(20))
    params = Column(JSON, nullable=False, default={})
    display_order = Column(Integer)
    is_active = Column(Boolean, nullable=False, default=True)
    is_work = Column(Boolean, nullable=False, default=False)
    exclude_load = Column(Boolean, nullable=False, default=False)

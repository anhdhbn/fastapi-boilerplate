from enum import Enum, IntEnum


class ContentTypeEnum(Enum):
    ApplicationJson = 'application/json'

class JaegerModeEnum(Enum):
    ThriftCollector = 'thrift-collector'
    ThriftAgent = 'thrift-agent'
    Grpc = 'grpc'

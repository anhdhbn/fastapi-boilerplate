class ErrorCode(object):
    SUCCESS_0000 = '0000'

    # 6xxx validate err
    ERROR_6000_NOT_FOUND = '6000'
    ERROR_6001_WRONG_DATA_TYPE = '6001'
    ERROR_6002_IS_INVALID = '6002'
    ERROR_6003_DATA_REQUIRE = '6003'
    ERROR_6004_DATA_MAX_LENGTH = '6004'
    ERROR_6005_EXCEEDED_MAX_DATE = '6005'
    ERROR_6006_A_GE_B = '6006'
    ERROR_6007_LENGTH_A_GE = '6007'
    ERROR_6008_LENGTH_A_LE = '6008'
    ERROR_6009_DUPLICATED = '6009'
    ERROR_6010_EXISTED = '6010'
    ERROR_6011_A_GE = '6011'
    ERROR_6012_A_LE = '6012'

    # 7xxx specific validate
    ERROR_7000_FILE_NO_DATA = '7000'
    ERROR_7001_MORE_THAN_X_ROWS = '7001'
    ERROR_7002_FILE_IMPORTED = '7002'
    ERROR_7003_HEADER_INVALID = '7003'

    # 8xxx external service error
    ERROR_8999_CANNOT_CONNECT_TO_UNKNOWN_SERVICE = '8999'

    # 9xx internal server error
    ERROR_9999_INTERNAL_SERVER_ERROR = '9999'

PYDANTIC_ERROR_MAPPING = {
    'value_error.number.not_ge': ErrorCode.ERROR_6011_A_GE,
    'value_error.number.not_le': ErrorCode.ERROR_6012_A_LE,
    'type_error.integer': ErrorCode.ERROR_6002_IS_INVALID,
    'type_error.list': ErrorCode.ERROR_6002_IS_INVALID,
    'value_error.missing': ErrorCode.ERROR_6000_NOT_FOUND,
    'value_error.any_str.min_length': ErrorCode.ERROR_6007_LENGTH_A_GE,
    'value_error.any_str.max_length': ErrorCode.ERROR_6008_LENGTH_A_LE,
    'type_error.enum': ErrorCode.ERROR_6002_IS_INVALID,
    'value_error.date': ErrorCode.ERROR_6002_IS_INVALID,
    'value_error.str.regex': ErrorCode.ERROR_6002_IS_INVALID,
}

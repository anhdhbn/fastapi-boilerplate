LOGGING_CONF = {
    'version': 1,
    'disable_existing_loggers': False,
    'filters': {
        'correlation_id': {
            '()': 'asgi_correlation_id.CorrelationIdFilter',
            'uuid_length': 32,
        },
    },
    'formatters': {
        'generic': {
            'class': 'logging.Formatter',
            'datefmt': '%Y-%m-%d %H:%M:%S',
            'format': '%(levelname)-10.10s %(asctime)s.%(msecs)03d [traceid=%(correlation_id)s][%(name)s][%(module)s:%(lineno)d] %(message)s',
        },
    },
    'handlers': {
        'console': {
            'class': 'logging.StreamHandler',
            'level': 'INFO',
            'formatter': 'generic',
            'filters': ['correlation_id'],
        },
    },

    'loggers': {
        'root': {
            'level': 'WARN',
            'handlers': ['console'],
        },
        'app': {
            'level': 'DEBUG',
            'handlers': ['console'],
            'qualname': 'app',
            'propagate': False,
        },
    },
}

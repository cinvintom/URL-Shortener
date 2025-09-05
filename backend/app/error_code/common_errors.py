class CommonErrorCode:
    """
    Error Code range: 1000 - 2000
    """
    INVALID_URL = 1000
    INTERNAL_SERVER_ERROR = 1001
    SHORT_URL_NOT_FOUND = 1002
    CUSTOM_URL_ALREADY_EXISTS = 1003
class CommonErrorCatalog:
    error_mapping = {
        CommonErrorCode.INVALID_URL: {
            "msg": "Invalid URL",
            "type": "invalid.url",
            "error_code": CommonErrorCode.INVALID_URL
        },
        CommonErrorCode.INTERNAL_SERVER_ERROR: {
            "msg": "Internal Server Error",
            "type": "internal.server.error",
            "error_code": CommonErrorCode.INTERNAL_SERVER_ERROR
        },
        CommonErrorCode.SHORT_URL_NOT_FOUND: {
            "msg": "Short URL not found",
            "type": "short.url.not.found",
            "error_code": CommonErrorCode.SHORT_URL_NOT_FOUND
        },
        CommonErrorCode.CUSTOM_URL_ALREADY_EXISTS: {
            "msg": "Custom URL already exists",
            "type": "custom.url.already.exists",
            "error_code": CommonErrorCode.CUSTOM_URL_ALREADY_EXISTS
        }
    }


common_error_catalog = CommonErrorCatalog()
from fastapi import HTTPException

from app.error_code.common_errors import CommonErrorCatalog

class ErrorManager:
    @staticmethod
    def error_responder(
        status_code: int,
        error_code: int,
        error_message: str = None
    ):
        error_response = HTTPException(status_code=None, detail=[])
        error_response.status_code = status_code

        error_catalog = {
            **CommonErrorCatalog.error_mapping,
        }
        error_response.detail.append(error_catalog[error_code])
        if error_message and error_response.detail:
            error_response.detail[0]["msg"] = error_message
        return error_response


error_manager = ErrorManager()

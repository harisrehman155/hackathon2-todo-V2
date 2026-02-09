from fastapi import HTTPException


def bad_request(message: str) -> HTTPException:
    return HTTPException(status_code=400, detail={"error": message, "code": "bad_request"})


def unauthorized(message: str = "Unauthorized") -> HTTPException:
    return HTTPException(status_code=401, detail={"error": message, "code": "unauthorized"})


def not_found(message: str = "Task not found") -> HTTPException:
    return HTTPException(status_code=404, detail={"error": message, "code": "not_found"})

from starlette.middleware.base import BaseHTTPMiddleware
from starlette.requests import Request
from services.logger import log_to_db

class LoggingMiddleware(BaseHTTPMiddleware):
    """
    Middleware to automatically log all incoming requests and outgoing responses
    into the database.
    """

    async def dispatch(self, request: Request, call_next):
        # Step 1: Read the incoming request body
        request_body = await request.body()

        try:
            request_data = request_body.decode('utf-8')
        except Exception:
            request_data = "<Unable to decode request>"

        # Step 2: Pass the request to the next handler
        response = await call_next(request)

        # Step 3: Read outgoing response body
        response_body = b""
        async for chunk in response.body_iterator:
            response_body += chunk

        # Step 4: Redefine the response.body_iterator as an async generator
        async def aiter_body():
            yield response_body

        response.body_iterator = aiter_body()

        try:
            response_data = response_body.decode('utf-8')
        except Exception:
            response_data = "<Unable to decode response>"

        # Step 5: Log to database
        log_to_db(request_data=request_data, response_data=response_data)

        return response

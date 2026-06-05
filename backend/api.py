import logging

from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, Field

from ai_service import AIQueryService

logging.basicConfig(level=logging.INFO)


class QueryRequest(BaseModel):
    question: str = Field(..., min_length=1, description="Natural language question for the AI query service")


class AIQueryAPI:
    def __init__(self, service: AIQueryService | None = None):
        self._service = service
        self.app = FastAPI(title="AI Query API", version="1.0.0")
        self._register_routes()

    def get_service(self) -> AIQueryService:
        if self._service is None:
            self._service = AIQueryService()
        return self._service

    def _register_routes(self):
        @self.app.get("/api/health")
        def health_check():
            return {"status": "ok"}

        @self.app.post("/api/prompt")
        def query(request: QueryRequest):
            try:
                service = self.get_service()
                response = service.query(request.question)
                payload = {"answer": str(response)}

                if hasattr(response, "metadata"):
                    metadata = response.metadata
                    if "sql_query" in metadata:
                        payload["sql_query"] = metadata["sql_query"]
                    if "result" in metadata:
                        payload["raw_result"] = metadata["result"]
                return payload
            except Exception as exc:
                logging.exception("Query failed")
                raise HTTPException(status_code=500, detail=str(exc)) from exc


api = AIQueryAPI()
app = api.app
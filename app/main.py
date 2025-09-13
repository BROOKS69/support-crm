from fastapi import FastAPI
from app import models, database
from app.routers import customers, auth

# Create database tables
models.Base.metadata.create_all(bind=database.engine)

# Initialize app
app = FastAPI(title="Support CRM Backend")

# Include routers
app.include_router(customers.router, prefix="/customers", tags=["Customers"])
# TODO: Implement other routers
# app.include_router(tickets.router, prefix="/tickets", tags=["Tickets"])
# app.include_router(logs.router, prefix="/logs", tags=["Communication Logs"])
# app.include_router(reports.router, prefix="/reports", tags=["Reports"])

@app.get("/")
def root():
    return {"message": "Welcome to Support CRM Backend API"}

from fastapi import FastAPI
from .routers import rfp_router, vendor_router, communication_router, proposal_router
from .database import init_db
from fastapi.middleware.cors import CORSMiddleware
from fastapi_utils.tasks import repeat_every
from .email_polling import check_inbox_and_process_replies


app = FastAPI(title="AI-Powered RFP Management (FastAPI)")

app.include_router(rfp_router.router, prefix="/api/rfps", tags=["RFP"])
app.include_router(vendor_router.router, prefix="/api/vendors", tags=["Vendors"])
app.include_router(communication_router.router, prefix="/api/communications", tags=["Communication"])
app.include_router(proposal_router.router, prefix="/api/proposals", tags=["Proposals"]) 

app.add_middleware( 
    CORSMiddleware,
    allow_origins=["*"],  # for testing
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.on_event("startup")
@repeat_every(seconds=2)
def poll_email_replies_task() -> None:
    init_db()
    check_inbox_and_process_replies()



# @app.on_event("startup")


# def startup():
#     init_db()
# # 
# @repeat_every(seconds=2)  # check inbox every 60 seconds
# def poll_email_replies_task() -> None:
#     check_inbox_and_process_replies()
# init_db()

# @app.get("/")
# async def root():
#     return {"status": "ok", "message": "RFP AI backend running"}

@app.get("/")
def root():
    print("Server is working")
    return {"message": "Server is working"}
 


#  uvicorn app.main:app --reload 
# venv\Scripts\activate

# "C:\Program Files\Python311\python.exe" -m venv venv
# & "C:\Users\manis\AppData\Local\Programs\Python\Python311\python.exe" -m venv venv


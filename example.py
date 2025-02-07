import os  # noqa: INP001

from fastapi import Depends, FastAPI, Security

from fastapi_auth0 import Auth0, Auth0User  # noqa: TC002

auth0_domain = os.getenv("AUTH0_DOMAIN", "")
auth0_api_audience = os.getenv("AUTH0_API_AUDIENCE", "")

auth = Auth0(
    domain=auth0_domain,
    api_audience=auth0_api_audience,
    scopes={"read:blabla": "Read BlaBla resource"},
)
app = FastAPI()


@app.get("/public")
async def get_public() -> dict:
    return {"message": "Anonymous user"}


@app.get("/secure", dependencies=[Depends(auth.implicit_scheme)])
async def get_secure(user: Auth0User = Security(auth.get_user)) -> dict:  # noqa: B008
    return {"message": f"{user}"}


@app.get("/secure/blabla", dependencies=[Depends(auth.implicit_scheme)])
async def get_secure_scoped(user: Auth0User = Security(auth.get_user, scopes=["read:blabla"])) -> dict:  # noqa: B008
    return {"message": f"{user}"}


@app.get("/secure/blabla2")
async def get_secure_scoped2(user: Auth0User = Security(auth.get_user, scopes=["read:blabla"])) -> dict:  # noqa: B008
    return {"message": f"{user}"}

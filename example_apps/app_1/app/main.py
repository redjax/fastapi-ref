"""
Example FastAPI app created by following the docs.

I've spiced it up a bit by separating things into modules as I go, using some
of my own favorite libraries (like Dynaconf instead of Pydantic for settings management).
"""
from typing import Annotated
import stackprinter

stackprinter.set_excepthook(style="darkbg2")

from red_utils.loguru_utils import init_logger
from loguru import logger as log

from config import settings, api_settings
from fastapi import FastAPI, status, Body, Form, HTTPException, Depends, Header
from fastapi.middleware.cors import CORSMiddleware

from fastapi.responses import JSONResponse

from domain.user import schemas as user_schemas
from domain.item import schemas as item_schemas

## Build an enum of tags
#  https://fastapi.tiangolo.com/tutorial/path-operation-configuration/#tags-with-enums
from lib.constants import Tags

## Convert objects to JSON
#  https://fastapi.tiangolo.com/tutorial/encoder/
from fastapi.encoders import jsonable_encoder

init_logger()

log.info(
    f"App Settings:\n\tHost={api_settings.api_host}\n\tPORT={api_settings.api_port}\n\tReload={api_settings.api_reload}"
)


async def common_parameters(q: str | None = None, skip: int = 0, limit: int = 100):
    """Inject a common dependency, with parameters shared to any endpoint that calls as a depend.

    https://fastapi.tiangolo.com/tutorial/dependencies/
    """
    return {"q": q, "skip": skip, "limit": limit}


## https://fastapi.tiangolo.com/tutorial/dependencies/#share-annotated-dependencies
#  Inject with:
#    async def some_func(commons: CommonsDep)
CommonsDep = Annotated[dict, Depends(common_parameters)]

## Fake db (list of dicts)
fake_items_db = [{"item_name": "Foo"}, {"item_name": "Bar"}, {"item_name": "Baz"}]


class CommonQueryParams:
    """Use a class as a dependency.
    https://fastapi.tiangolo.com/tutorial/dependencies/classes-as-dependencies/

    Inject with:
      async def some_function(commons: Annotated[CommonQueryParams, Depends(CommonQueryParams)])
    """

    def __init__(self, q: str | None = None, skip: int = 0, limit: int = 100):
        self.q = self.skip = skip
        self.limit = limit


## Create functions to validate header tokens, and raise exceptions
#  https://fastapi.tiangolo.com/tutorial/dependencies/dependencies-in-path-operation-decorators/#raise-exceptions
async def verify_token(x_token: Annotated[str, Header()]):
    """Validate X-Token parameter.

    Expected value: {"X-Token": "fake-token"}
    """
    if x_token != "fake-token":
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail="X-Token header invalid"
        )

    raise x_token


async def verify_key(x_key: Annotated[str, Header()]):
    """Validate X-Key parameter.

    Expected value: {"X-TKey": "fake-key"}
    """
    if x_key != "fake-key":
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail="X-Key header invalid"
        )

    return x_key


## Initialize FastAPI app
app = FastAPI()

## Alternatively, inject verify_key()/verify_token() as "global" depends,
#  requiring a header with valid X-Key and X-Token values
# app = FastAPI(dependencies=[Depends(verify_token), Depends(verify_key)])

app.add_middleware(
    CORSMiddleware,
    allow_origins=api_settings.api_origins or ["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


## Add a summary & description to endpoint
#  https://fastapi.tiangolo.com/tutorial/path-operation-configuration/#summary-and-description
@app.get(
    "/",
    summary="Root path",
    description="An empty endpoint that simply returns a success response",
)
## Depends() can be declared in Annotated, i.e. Annotated[Object, Depends()] is equivalent
#    to Annotated[Object, Depends(Object)]
async def hello_world(commons: Annotated[CommonQueryParams, Depends()]):
    content = {"message": "Hello world!"}

    ## Serialize & return the response
    return JSONResponse(status_code=status.HTTP_200_OK, content=content)


## Demo endpoint with dependencies to validate X-Token & X-Key headers
@app.get("/validate-headers", dependencies=[Depends(verify_token), Depends(verify_key)])
async def validate_headers():
    return [{"item": "Foo"}, {"item": "Bar"}]


## Demo endpoint with a Dependency injected.
#  The dependency is CommonQueryParams, a class defined above.
#  Dependencies can also be injected in the path operation decorated:
#    https://fastapi.tiangolo.com/tutorial/dependencies/dependencies-in-path-operation-decorators/#add-dependencies-to-the-path-operation-decorator
@app.get(
    "/common-ex",
    summary="Demo a Class dependency.",
    description="Demo the CommonQueryParams class Depend (example from docs)",
)
async def common_ex(commons: Annotated[CommonQueryParams, Depends()]):
    ## Prepare an empty response
    response = {}

    ## If a query is present
    if commons.q:
        ## Update response with the query
        response.updated({"q": commons.q})

    ## Create list of items, skipping num from commons.skip x times, where x = commons.limit
    items = fake_items_db[commons.skip : commons.skip + commons.limit]

    ## Update the response with remaining items
    response.update({"items": items})

    return response


## Use response_model_exclude_unset to only return non-null fields
#  https://fastapi.tiangolo.com/tutorial/response-model/#use-the-response_model_exclude_unset-parameter
## Status_code docs: https://fastapi.tiangolo.com/tutorial/response-status-code/#response-status-code
## Tags: https://fastapi.tiangolo.com/tutorial/path-operation-configuration/#tags
@app.put(
    "/users",
    response_model=user_schemas.UserBase,
    response_model_exclude_unset=True,
    response_model_exclude_defaults=True,
    status_code=status.HTTP_201_CREATED,
    tags=[Tags.users],
    response_description="The created User, without their password",
)
async def add_user(
    user: Annotated[user_schemas.User, Body(embed=True)]
) -> user_schemas.UserBase:
    log.debug(f"Incoming User: {user}")
    _user = user_schemas.User.model_validate(user)

    ## Convert objects to JSON
    #  https://fastapi.tiangolo.com/tutorial/encoder/
    user = jsonable_encoder(_user)

    return user


## Handling form fields
#  https://fastapi.tiangolo.com/tutorial/request-forms/
@app.post("/login/", tags=[Tags.users])
async def login(username: Annotated[str, Form()], password: Annotated[str, Form()]):
    return {"username": username}


## Handling errors
#  https://fastapi.tiangolo.com/tutorial/handling-errors/#raise-an-httpexception-in-your-code
@app.get("/items/{item_id}", tags=[Tags.items])
async def read_item(item_id: str):
    items = {"test": "This is a test item"}

    if item_id not in items:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Item with ID {item_id} not found.",
            headers={"X-Error": "Item not found"},
        )

    return {"item": items[item_id]}


## Partial updates using Pydantic's exclude_unset
#  https://fastapi.tiangolo.com/tutorial/body-updates/#partial-updates-with-patch
@app.patch(
    "/items/{item_id}",
    response_model=item_schemas.ItemBase,
    response_model_exclude_unset=True,
    tags=[Tags.items],
)
async def update_item(item_id: str, item: item_schemas.Item):
    """Update an item by making a copy of the schema, excluding unset/absent values.

    Overwrite the original with the copy.
    """

    ## Example "database", a dict of dict objects
    #  The objects are varying degrees of complete,
    #  to demo different PATCH requests.
    items = {
        "foo": {"name": "Foo", "price": 50.2},
        "bar": {
            "name": "Bar",
            "description": "The bartenders",
            "price": 62,
            "tax": 20.2,
            "tags": ["tag1", "tag2"],
        },
        "baz": {
            "name": "Baz",
            "description": None,
            "price": 50.2,
            "tax": 10.5,
            "tags": ["tag1", "tag3"],
        },
    }

    log.debug(f"Item: {items[item_id]}")

    ## Retrieve item by ID
    stored_item_data = items[item_id]
    ## Create schema
    stored_item_model = item_schemas.Item(**stored_item_data)
    ## Dump model to dict, excluding unset values
    update_data = item.model_dump(exclude_unset=True)
    ## Update object by creating a copy, updating data as copy runs
    updated_item = stored_item_model.model_copy(update=update_data)
    log.debug(f"Updated item: {updated_item}")

    items[item_id] = jsonable_encoder(updated_item)

    return updated_item

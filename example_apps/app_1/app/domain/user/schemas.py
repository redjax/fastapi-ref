from pydantic import BaseModel, Field


class UserGroup(BaseModel):
    number: int | None = Field(
        default=None, title="Group number for indexing/searching", gt=0
    )
    name: str | None = Field(default=None, title="Name of group", max_length=264)


class UserBase(BaseModel):
    """Nested models:
    https://fastapi.tiangolo.com/tutorial/body-nested-models/

    Return type & data filtering docs:
    https://fastapi.tiangolo.com/tutorial/response-model/#return-type-and-data-filtering
    """

    first_name: str | None = Field(
        default=None, title="User's first name", max_length=100, examples=["Foo"]
    )
    last_name: str | None = Field(
        default=None, title="User's last name", max_length=200, examples=["Bar"]
    )
    age: int | None = Field(
        default=None, title="User's age", gt=0, lt=120, examples=[20]
    )
    ## Set docs: https://fastapi.tiangolo.com/tutorial/body-nested-models/#set-types
    tags: set[str] | None = Field(
        default=set(), title="User tags", examples=[("tag1", "tag2")]
    )
    ## Nested models: https://fastapi.tiangolo.com/tutorial/body-nested-models/#nested-models
    #  Also, list of submodels: https://fastapi.tiangolo.com/tutorial/body-nested-models/#attributes-with-lists-of-submodels
    groups: list[UserGroup] | None = Field(
        default=[],
        title="List of Groups this User is a member of",
        examples=[[{"number": 1, "name": "ExampleGroup"}]],
    )

    ## Instead of using model_config below, you can add examples=[] to each field above.
    #  model_config docs:
    #    https://fastapi.tiangolo.com/tutorial/schema-extra-example/#extra-json-schema-data-in-pydantic-models

    # model_config = {
    #     "json_schema_extra": {
    #         "examples": [
    #             {
    #                 "first_name": "Foo",
    #                 "last_name": "Bar",
    #                 "age": 24,
    #                 "tags": ["example", "example2"],
    #                 "groups": [
    #                     {"number": 1, "name": "Admins", "number": 2, "name": "Remote"}
    #                 ],
    #             }
    #         ]
    #     }
    # }


class User(UserBase):
    password: str | None = Field(
        default=None,
        title="User's password. Must be at least 16 characters",
        min_length=16,
        examples=["Th1sis@vErySEcureP4ssw0rd!"],
    )

from datetime import datetime
from ...models import User
from ...models.user import TermsAndConditions
from ...errors import UserDoesNotExistError
from ...repos import UserDBRepo, EOXRepo
from .retrieve_user import retrieve_user

def accept_user_terms_and_conditions(user):
    repo, eox_repo = UserDBRepo(), EOXRepo()
    # check user exists
    data = retrieve_user(user.uid).dict()
    # generate credentials
    errors = eox_repo.generate_credentials(user.uid, user.email)
    print(errors)
    if len(errors) > 0:
        raise Exception(errors)
    # update user
    data.update(
        terms=TermsAndConditions(
            geodb=True, sentinelhub=True, eotdl=True, eoxhub=True
        ),
        updatedAt=datetime.now(),
    )
    user = User(**data)
    repo.update_user(data["_id"], user.dict())
    return user

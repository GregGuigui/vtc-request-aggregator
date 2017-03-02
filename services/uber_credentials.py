import utils
import services.uber_authorize_user as authorize_user
from app import app, env

credentials = utils.import_app_credentials("app/config/config_uber." + env + ".yml")
auth_flow = authorize_user.get_auth_flow(credentials)
uber_url = authorize_user.authorization_code_grant_flow(auth_flow)
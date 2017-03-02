import utils
import services.lyft_authorize_user as authorize_user
from app import app, env

credentials = utils.import_app_credentials("app/config/config_lyft." + env + ".yml")
auth_flow = authorize_user.get_auth_flow(credentials)
lyft_url = authorize_user.authorization_code_grant_flow(auth_flow)
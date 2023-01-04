from os import environ as env
from dotenv import find_dotenv, load_dotenv
from functools import wraps

from flask import Flask, redirect, render_template, session, url_for, request, jsonify

load_dotenv(find_dotenv())
AUTH0_CLIENT_SECRET = env.get("AUTH0_CLIENT_SECRET")

def get_auth_header():
    header = request.headers.get("Authorization", None)

    if not header:
        return jsonify(error="Authorization header is expected", status=401)
    
    header_split = header.split()

    if header_split[0].lower() != "bearer":
        return jsonify(error="Authorization header must start with Bearer", status=401)

    elif len(header_split) == 1:
        return jsonify(error="Token not found", status=401)
    
    return jsonify(message="success", data={'token': header_split[1]}, status=200)


def requires_auth(func):
    """Determines if the access token is valid
    """
    
    # @wraps(func)
    # def decorated(*args, **kwargs):
    #     token = get_auth_header()
    #     jsonurl = urlopen("https://" + AUTH0_DOMAIN + "/.well-known/jwks.json")
    #     jwks = json.loads(jsonurl.read())
    #     try:
    #         unverified_header = jwt.get_unverified_header(token)
    #     except jwt.JWTError as jwt_error:
    #         raise AuthError({"code": "invalid_header",
    #                         "description":
    #                             "Invalid header. "
    #                             "Use an RS256 signed JWT Access Token"}, 401) from jwt_error
    #     if unverified_header["alg"] == "HS256":
    #         raise AuthError({"code": "invalid_header",
    #                          "description":
    #                              "Invalid header. "
    #                              "Use an RS256 signed JWT Access Token"}, 401)
    #     rsa_key = {}
    #     for key in jwks["keys"]:
    #         if key["kid"] == unverified_header["kid"]:
    #             rsa_key = {
    #                 "kty": key["kty"],
    #                 "kid": key["kid"],
    #                 "use": key["use"],
    #                 "n": key["n"],
    #                 "e": key["e"]
    #             }
    #     if rsa_key:
    #         try:
    #             payload = jwt.decode(
    #                 token,
    #                 rsa_key,
    #                 algorithms=ALGORITHMS,
    #                 audience=API_IDENTIFIER,
    #                 issuer="https://" + AUTH0_DOMAIN + "/"
    #             )
    #         except jwt.ExpiredSignatureError as expired_sign_error:
    #             raise AuthError({"code": "token_expired",
    #                             "description": "token is expired"}, 401) from expired_sign_error
    #         except jwt.JWTClaimsError as jwt_claims_error:
    #             raise AuthError({"code": "invalid_claims",
    #                             "description":
    #                                 "incorrect claims,"
    #                                 " please check the audience and issuer"}, 401) from jwt_claims_error
    #         except Exception as exc:
    #             raise AuthError({"code": "invalid_header",
    #                             "description":
    #                                 "Unable to parse authentication"
    #                                 " token."}, 401) from exc

    #         _request_ctx_stack.top.current_user = payload
    #         return func(*args, **kwargs)
    #     raise AuthError({"code": "invalid_header",
    #                      "description": "Unable to find appropriate key"}, 401)

    # return decorated
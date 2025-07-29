# import httpx
# from blacksheep import Request
# from guardpost import AuthenticationHandler, Identity
# from jose import jwt
#
# from .models import User
#
#
# PUBLIC_KEY_CACHE_TIMEOUT = 24 * 60 * 60  # 24 hours
#
#
# def get_kc_public_keys(client_id: str, server_url: str, realm: str) -> dict[str, dict]:
#     response = httpx.get(f"{server_url}/realms/{realm}/protocol/openid-connect/certs", timeout=5)
#     return {key["kid"]: key for key in response.json()["keys"]}
#
#
# def get_dummy_user():
#     # Create dummy sqlalchemy User record and return it
#
#
# class DummyAuthentication(AuthenticationHandler):
#     def authenticate(self, request: Request) -> tuple[User, None]:
#         request.user = get_dummy_user()
#         return request.user, None
#
#     def authenticate_header(self, request: Request) -> str:
#         return ""
#
#
# class KeycloakAuthentication(BaseAuthentication):
#     @staticmethod
#     def find_public_key_and_realm(client_id: str, kid: str) -> tuple[dict, str]:
#         match client_id:
#             case settings.SSO_CLIENT_ID:
#                 realm = settings.SSO_CLIENT_REALM
#             case settings.SA_CLIENT_ID:
#                 realm = settings.SA_CLIENT_REALM
#             case _:
#                 raise exceptions.AuthenticationFailed(f"Unknown client: {client_id}")
#
#         if public_key := get_kc_public_keys(client_id, settings.KEYCLOAK_SERVER_URL, realm).get(kid):
#             return public_key, realm
#
#         raise exceptions.AuthenticationFailed("Invalid token.")
#
#     def authenticate(self, request: Request) -> tuple[User | None, None]:
#         auth_header = str(request.META.get("HTTP_AUTHORIZATION", b""))
#         if not auth_header.startswith("Bearer "):
#             # The UI expects a 401 when the user is not authenticated,
#             # so we raise the exception here instead of returning
#             # None which would result in a 403
#             raise exceptions.AuthenticationFailed("You must be authenticated to access this endpoint")
#         token = auth_header.split("Bearer ")[1].strip()
#
#         try:
#             header = jwt.get_unverified_header(token)
#             body = jwt.get_unverified_claims(token)
#             kid = header["kid"]
#             client_id = body["azp"]
#             public_key, realm = self.find_public_key_and_realm(client_id, kid)
#
#             decoded_token = jwt.decode(
#                 token,
#                 public_key,
#                 algorithms=["RS256"],
#                 options={"verify_aud": False, "verify_signature": True, "verify_exp": True},
#             )
#
#             email = ""
#             username = decoded_token["preferred_username"]
#             if "email" in decoded_token:
#                 email = decoded_token["email"]
#                 name = decoded_token["given_name"] + " " + decoded_token["family_name"]
#             else:
#                 # Client credentials flow, no email
#                 name = decoded_token["clientId"]
#             roles: list[str] = decoded_token.get("user-roles", [])
#             user, _ = User.objects.get_or_create(
#                 username=username,
#                 defaults={
#                     "name": name,
#                     "issuer": decoded_token["iss"],
#                     "realm": realm,
#                     "email": email,
#                 },
#             )
#
#             user.ad_roles = decoded_token.get("ad_roles", [])
#             user.roles = roles
#             request.user = user
#
#             return user, None
#         except jwt.ExpiredSignatureError as e:
#             raise exceptions.AuthenticationFailed("Token has expired.") from e
#         except jwt.JWTError as e:
#             raise exceptions.AuthenticationFailed("Invalid token.") from e
#         except Exception as e:
#             raise exceptions.AuthenticationFailed("Invalid token.") from e
#
#     def authenticate_header(self, request: Request) -> str:
#         realms = []
#         if settings.SA_CLIENT_REALM:
#             realms.append(settings.SA_CLIENT_REALM)
#         if settings.SSO_CLIENT_REALM:
#             realms.append(settings.SSO_CLIENT_REALM)
#         return f'Bearer realm="{"|".join(realms)}"'

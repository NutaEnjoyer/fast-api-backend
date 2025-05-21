from fastapi import Request, HTTPException, Cookie

from app.core.security import ACCESS_TOKEN_COOKIE_NAME, decode_token

async def get_current_user(request: Request) -> str:
    print(request.base_url)
    print(request.cookies)
    access_token = request.cookies.get(ACCESS_TOKEN_COOKIE_NAME)

    print(access_token)
    if not access_token:
        raise HTTPException(status_code=401, detail="Unauthorized")
    
    decode = decode_token(access_token)
    print("DECODE: ", decode, "_END")

    user_id = decode.get("id")

    print(user_id)

    return user_id


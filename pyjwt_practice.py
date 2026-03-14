import jwt
payload={"user_1":1} #pyjwt expects dictionary as payload
secret="HMAC_KEY_FOR_HS256_SHOULD_BE_MIN_32_BYTES"
token=jwt.encode(
    payload,
    key=secret,
    algorithm="HS256"
)
print(token)

payload=jwt.decode(token,key=secret,algorithms="HS256")
print(payload)

token=jwt.decode_complete(token,key=secret,algorithms="HS256")
#returns all the information int the format
#{payload,header,signature}

print(token)
 
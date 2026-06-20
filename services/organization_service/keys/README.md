# JWT verification key

This folder holds the **public** half of `auth_service`'s RSA signing keypair, used here only to verify JWTs — this service never signs tokens, only checks them.

- `jwt_public.pem` — copied from `services/auth_service/keys/jwt_public.pem`. Safe to share/commit in principle, but it's gitignored (`*.pem`) for consistency with the private key — this README is what's actually tracked, so the folder still shows up for anyone cloning the repo.

There is no private key here, and there never should be — this service has no business signing tokens.

## Getting the key

Copy it from `auth_service`:

```bash
cp ../auth_service/keys/jwt_public.pem keys/jwt_public.pem
```

If `auth_service`'s key is rotated, re-copy it here — verification breaks until you do.

## Pointing the app at the key

In `.env`:

```
JWT_PUBLIC_KEY_PATH=keys/jwt_public.pem
JWT_ALGORITHM=RS256
```

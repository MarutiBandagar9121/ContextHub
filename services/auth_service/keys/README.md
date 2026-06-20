# JWT signing keys

This folder holds the RSA keypair `auth_service` uses to sign JWTs (`RS256`).

- `jwt_private.pem` — signs tokens. **Lives only here.** Never commit it, never copy it to another service.
- `jwt_public.pem` — verifies tokens. Safe to share — copy it into any other service that needs to verify tokens issued by this service (e.g. `services/organization_service/keys/jwt_public.pem`).

Both `.pem` files are gitignored (`*.pem` in the root `.gitignore`) — this README is the only thing in this folder that's actually committed, so the folder and its purpose show up for anyone cloning the repo.

## Generating a keypair

From this service's root (`services/auth_service/`), using Git Bash (or any shell with `openssl` on PATH):

```bash
openssl genrsa -out keys/jwt_private.pem 2048
openssl rsa -in keys/jwt_private.pem -pubout -out keys/jwt_public.pem
```

Then copy `keys/jwt_public.pem` into every other service that verifies this service's tokens.

## Pointing the app at the keys

In `.env`:

```
JWT_PRIVATE_KEY_PATH=keys/jwt_private.pem
JWT_PUBLIC_KEY_PATH=keys/jwt_public.pem
JWT_ALGORITHM=RS256
```

## Rotating keys

Generate a new pair, redistribute the new public key to every verifying service, then swap the private key here. Tokens signed with the old key stop verifying the moment any service updates its public key — so rotate during a deploy window, not mid-day, until a JWKS endpoint (multiple valid keys at once) is in place.

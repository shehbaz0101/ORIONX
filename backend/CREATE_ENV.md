# Creating backend/.env File

Since `.env` files are gitignored (for security), you need to create it manually.

## Quick Setup

1. **Copy the example file:**
   ```bash
   cd backend
   cp .env.example .env
   ```

2. **Or create it manually:**
   - Copy contents from `backend/.env.example`
   - Create new file `backend/.env`
   - Paste the contents
   - Fill in actual values

## Values to Fill

Replace these placeholders with actual values:

- `[PASSWORD]` → Your Supabase database password
- `[PROJECT_REF]` → Your Supabase project reference ID
- `[ENDPOINT]` → Your Upstash Redis endpoint
- `[PORT]` → Your Upstash Redis port
- `[YOUR_API_KEY]` → Your OpenRouter API key
- `[YOUR_SUPABASE_SERVICE_ROLE_KEY]` → Your Supabase service role key
- `[YOUR_SUPABASE_ANON_KEY]` → Your Supabase anonymous key
- `[GENERATE_A_RANDOM_32_CHAR_STRING]` → Generate with: `python -c "import secrets; print(secrets.token_urlsafe(32))"`

## For Railway Deployment

For Railway, you don't need a local `.env` file. Instead:
1. Go to Railway Dashboard
2. Select your service
3. Go to **Variables** tab
4. Add all variables from `backend/.env.example`

## For Local Development

1. Copy `backend/.env.example` to `backend/.env`
2. Fill in values for local development
3. Use local PostgreSQL and Redis URLs if needed


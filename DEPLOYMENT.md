Deployment (production)
-----------------------

This repository includes Dockerfiles for the frontend and backend and a GitHub Actions workflow that builds and publishes images to GitHub Container Registry (GHCR).

Quick overview:

- GitHub Actions: `.github/workflows/ci.yml` — builds and pushes two images to `ghcr.io/<owner>/daily-expenses-tracker-backend` and `-frontend` on pushes to `main`.
- Docker Compose: `docker-compose.prod.yml` — example compose that pulls the published images and runs `mongo` for a self-contained deployment.
- Environment: use `.env.example` as a starting point; set `MONGO_URI` to your managed MongoDB connection string for production.

Deploy steps (recommended):

1. Push to `main` (already configured). The workflow will build and push images to GHCR.

2. On your production host (VM, droplet, server), install Docker and docker-compose.

3. Create a `.env` file using `.env.example` and set `MONGO_URI` to a production database.

4. Run the compose file to start services (it will pull published images from GHCR):

```bash
export GITHUB_USER=kannanvathi # or your org/user
docker-compose -f docker-compose.prod.yml up -d
```

Notes:
- For production, use a managed MongoDB instance (Atlas / DigitalOcean Managed DB) and set `MONGO_URI` accordingly.
- Optionally front the services with a reverse proxy (NGINX, Traefik) and enable TLS.
- If you want zero-downtime deploys, consider using a container orchestrator (Docker Swarm / Kubernetes / Render / Fly / AWS ECS).
 - If you want zero-downtime deploys, consider using a container orchestrator (Docker Swarm / Kubernetes / Render / Fly / AWS ECS).

Platform-specific quick guides

Vercel (frontend):

- Import the repository into Vercel (https://vercel.com/new) and select the `frontend` directory as the project root.
- Build Command: `npm run build`
- Output Directory: `dist`
- Add environment variables in the Vercel dashboard if your frontend needs to call the backend (e.g. `VITE_API_URL` set to your backend URL).

Render (backend):

- Use `render.yaml` included in the repo to create the web service for the backend. Render will detect the service defined in `render.yaml` when you connect the repo.
- The backend service runs using the included `backend/Dockerfile`. Set the `MONGO_URI` environment variable in Render to point to your production MongoDB (Atlas).
- Health check path: `/health` (implement simple health endpoint if not present).

MongoDB Atlas:

- Create a new cluster on MongoDB Atlas and create a database user.
- Copy the connection string (URI) and set it in Render as `MONGO_URI` and locally in your `.env` if testing.

Security note:

- Never commit real credentials to the repository. Use platform environment variables or secrets (Vercel/Render/Atlas) for production secrets.

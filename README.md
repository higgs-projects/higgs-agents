# Higgs Agents API

Welcome to the Higgs Agents API: a robust, production-ready application for serving AI Agents as an API. Built on FastAPI and Agno framework, it provides:
  * A **FastAPI server** with comprehensive middleware and extensions
  * **PostgreSQL with pgvector** for storing Agent sessions, knowledge, and vector data
  * **Multiple storage backends** support (Aliyun OSS, Tencent COS, Volcengine TOS, OpenDAL)
  * **Vector database integrations** (Chroma, Elasticsearch, Milvus, Weaviate, Tencent Vector)
  * **Pre-built Agents** with DeepSeek V3 integration via SiliconFlow
  * **Production-ready** configuration with monitoring, logging, and metrics

## Quickstart

Follow these steps to get your Agent API up and running:

> Prerequisites: [docker desktop](https://www.docker.com/products/docker-desktop) should be installed and running.

### Clone the repo

```sh
git clone https://github.com/higgs-agi/higgs-agents.git
cd higgs-agents
```

### Configure API keys and Environment Variables

The default agent uses DeepSeek V3 via SiliconFlow. Set the required environment variables:

```bash
export OPENAI_API_KEY="YOUR_API_KEY_HERE"
export DB_USER="ai"
export DB_PASSWORD="ai"
export DB_NAME="ai"
```

> **Note**: The agent is configured to use SiliconFlow's DeepSeek V3 endpoint by default. You can modify the agent configuration in `/api/agents/basic.py` to use other model providers.

### Start the application

Run the application using docker compose:

```bash
cd docker
docker compose up -d
```

This command starts:
* The **FastAPI server**, running on [http://localhost:8000](http://localhost:8000)
* The **PostgreSQL with pgvector** database, accessible on `localhost:5432`

Once started, you can:
* Test the API at [http://localhost:8000/docs](http://localhost:8000/docs).

### Connect to Agno Playground or Agent UI

* Open the [Agno Playground](https://app.agno.com/playground).
* Add `http://localhost:8000` as a new endpoint. You can name it `Higgs Agents` (or any name you prefer).
* Select your newly added endpoint and start chatting with your Agents.

### Stop the application

When you're done, stop the application using:

```sh
docker compose down
```

## Prebuilt Agents & Configurations

### Available Agents

The `/api/agents` folder contains pre-built agents:
- **Basic Agent**: Uses DeepSeek V3 via SiliconFlow with PostgreSQL storage
  - Features: Session history, message persistence, markdown responses
  - Configuration: Modify `api/agents/basic.py` for different models

### Supported Storage Backends
- **PostgreSQL**: Default storage with pgvector for embeddings
- **Cloud Storage**: Aliyun OSS, Tencent COS, Volcengine TOS, OpenDAL
- **Vector Databases**: Chroma, Elasticsearch, Milvus, Weaviate, Tencent Vector DB

### Configuration Structure
- `api/configs/`: Application configuration files
- `api/configs/middleware/`: Middleware configurations (cache, storage, VDB)
- `api/extensions/`: FastAPI extensions (logging, metrics, compression, etc.)

## Development Setup

To setup your local development environment:

### Install Dependencies with UV

The project uses `uv` for Python environment and package management. Install dependencies:

```bash
cd api
uv sync
```

### Run the Development Server

Start the development server with hot reload:

```bash
uvicorn app:app --host 0.0.0.0 --port 8000 --reload
```

### Run with Docker Compose (Recommended)

For a complete development environment with database:

```bash
cd docker
docker compose up -d
```

## Managing Python Dependencies

### Add New Dependencies

Add dependencies to `api/pyproject.toml` in the appropriate section:

```bash
cd api
uv add package-name
```

### Update Dependencies

Update all dependencies to latest compatible versions:

```bash
cd api
uv update
```

### Rebuild Docker Images

After updating dependencies, rebuild the Docker image:

```bash
cd docker
docker compose up -d --build
```

## Community & Support

Need help, have a question, or want to connect with the community?

* 📚 **[Read the Agno Docs](https://docs.agno.com)** for more in-depth information.
* 💬 **Chat with us on [Discord](https://agno.link/discord)** for live discussions.
* ❓ **Ask a question on [Discourse](https://agno.link/community)** for community support.
* 🐛 **[Report an Issue](https://github.com/higgs-agi/higgs-agents/issues)** on GitHub if you find a bug or have a feature request.

## Production Deployment

### Build Production Docker Image

Build the production image using the included Dockerfile:

```bash
docker build -t your-repo/higgs-agents:latest -f api/Dockerfile .
```

### Environment Variables for Production

Set these environment variables in your production environment:

```bash
OPENAI_API_KEY="your-api-key"
DB_HOST="your-production-db-host"
DB_PORT="5432"
DB_USER="your-db-user"
DB_PASS="your-db-password"
DB_DATABASE="your-db-name"
```

### Cloud Deployment Options

The application can be deployed to any container platform:

- **Cloud Run** (Google Cloud): Fully managed serverless containers
- **ECS/EKS** (AWS): Elastic Container Service or Kubernetes
- **AKS** (Azure): Azure Kubernetes Service
- **Railway/Render**: Simplified container deployment platforms

### Database Considerations

For production, use a managed PostgreSQL service:
- **AWS RDS**: Amazon Relational Database Service
- **Google Cloud SQL**: Managed PostgreSQL service
- **Azure Database for PostgreSQL**: Azure's managed offering
- Ensure pgvector extension is enabled for vector operations

### Monitoring and Observability

The application includes built-in extensions for:
- Application metrics (Prometheus format)
- Structured logging
- Request/response compression
- Timezone handling
- Exception handling
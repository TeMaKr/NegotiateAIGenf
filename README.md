# NegotiateAI

This is the repository of the NegotiateAI project.

## Structure

The project has the following structure.

```bash
docs/                         # Project documentation
frontend/                     # Frontend application built using Vue and Vuetify
├── Dockerfile                # Dockerfile for containerizing the frontend
├── env.d.ts                  # TypeScript environment definitions
├── eslint.config.js          # ESLint configuration for code linting
├── index.html                # Entry point for the frontend application
├── nginx.conf                # Nginx configuration for serving the frontend
├── package.json              # Node.js dependencies and scripts
├── README.md                 # Frontend documentation
├── tsconfig.*.json           # TypeScript configuration files
├── vite.config.mts           # Vite configuration for development and build
├── data/                     # Static data files
├── public/                   # Static assets (e.g., favicon, images)
└── src/                      # Source code for the frontend
    ├── App.vue               # Root Vue component
    ├── auto-imports.d.ts     # Auto-generated import definitions
    ├── components.d.ts       # Auto-generated component definitions
    ├── main.ts               # Application entry point
    ├── typed-router.d.ts     # Type definitions for router
    ├── assets/               # Project-specific assets
    ├── components/           # Reusable Vue components
    ├── composables/          # Vue composables
    ├── plugins/              # Vue plugins
    ├── router/               # Vue Router configuration
    ├── services/             # API services
    ├── stores/               # State management (Pinia)
    ├── styles/               # Global styles and SCSS settings
    └── views/                # Page views
orchestration/                # Backend services and orchestration
├── fastapi/                  # FastAPI backend
│   ├── docker-compose.yml    # Docker Compose configuration for FastAPI
│   ├── Dockerfile            # Dockerfile for containerizing FastAPI
│   ├── poetry.lock           # Poetry lock file for Python dependencies
│   ├── pyproject.toml        # Python project configuration
│   ├── README.md             # FastAPI documentation
│   └── src/                  # Source code for FastAPI
│       ├── __init__.py       # Package initialization
│       ├── api.py            # Main API application
│       ├── settings.py       # Application settings (pydantic-settings)
│       ├── worker.py         # Celery worker configuration
│       ├── data/             # Data files and storage
│       ├── models/           # Pydantic models for data validation
│       ├── routers/          # API routers for modular endpoints
│       ├── scraper/          # Web scraping modules
│       ├── scripts/          # Scripts which are run at start up of the application
│       ├── security/         # Authentication and security (rate limiting)
│       ├── tasks/            # Celery tasks for asynchronous processing
│       ├── tests/            # Test files
│       ├── tools/            # AI Tools and LLM integration
│       └── vector_database/  # Qdrant specific configurations/implementations
└── pocketbase/               # PocketBase backend
    ├── Dockerfile            # Dockerfile for PocketBase
    ├── pocketbase            # PocketBase executable
    ├── README.md             # PocketBase documentation
    ├── pb_data/              # PocketBase database and storage
    ├── pb_hooks/             # PocketBase hooks
    └── pb_migrations/        # Database migration files
terraform/                   # Infrastructure as Code for deployment
├── backend.tf               # Terraform backend configuration
├── Caddyfile.tftpl         # Caddy reverse proxy template
├── main.tf                 # Main Terraform configuration
├── variables.tf            # Terraform variables
└── environments/           # Environment-specific configurations
.gitlab-ci.yml               # CI/CD pipeline configuration for GitLab
Makefile                     # Makefile for managing common tasks
```

## Get Started

Please include the .env file with the current version. You need to replace the LLM Provider in the .env. API Key access is provided separately. Please reach out to Rahkakavee Baskaran if you need access to the .env file or the API Keys.

It is recommended to start first pocketbase and then fastapi backend.

To run the frontend first install all dependencies:

```bash
npm install
```

For development purposes you can run the frontend using:

```bash
npm run dev
```

To start pocketbase you need to download a suitable pocketbase executable here <https://pocketbase.io/docs/> and put it into the directory `pocketbase`. Navigate to the pocketbase folder. First export the API_FASTAPI_API__TOKEN value from the .env file to your environment using ```export API_FASTAPI_API__TOKEN=<your_token>```. Then start pocketbase using the following script:

```bash
cd orchestration/pocketbase
./pocketbase serve --http localhost:8090 --dev 
```

Alternatively you can use the Makefile and stay in the root file.

```bash
make pocketbase-start
```

If you run pocket base for the first time and open the dashboard you need to register. You can use a valid email address and password. After login you will be prompted to add a one time password. Go to the terminal where pocket base is running. You should see an email in the terminal with a one time password. Please use this one time password for registration. As long as you do not delete the pocketbase/pb_data/data.db you do not need to register again and you can login with your password.

**Before Starting docker compose** In order to correctly load the data into the database (data load starts with initializing of docker compose) you need to set the API_POCKETBASE_API__TOKEN value from the .env in the table api_tokens in pocketbase.
To run FastAPI and Celery you need to install docker. Please find more information on Docker here <https://docs.docker.com/desktop/>.
To start the FastAPI backend, first navigate to the fastapi folder. Since we need to install a cpu torch version which is not available for mac we need to first build the image with the correct name. Then use docker compose up to start the containers. Please make sure to first start pocketbase and then the docker containers. Note that one of the containers (negotiate_ai_scripts) runs the insert of historical data, the augmentation processes and the create of collections in Qdrant. This might take a while. If the data is already in pocketbase the container will throw a lot of HTTP Status Errors. This is intended. You can ignore this. In both cases: The container will stop and be removed automatically.

```bash
cd orchestration/fastapi
docker build --platform linux/amd64 -t negotiate_ai_app ./
docker compose up 
```

To stop and remove containers and networks use:

```bash
docker compose down
```

Please find more information on docker-compose here: <https://docs.docker.com/compose/>.

Alternatively you can use the Makefile and stay in the root file.

```bash
make fastapi-build
make fastapi-start
make fastapi-stop
```

## Architecture and Data Flows

You can find more information about the architecture and the data flows in docs/architecture.md

## Authentication

You can find an overview with all permissions to API and Database in docs/authentication_permissions.md

## Data Quality Checks

With the new scraping methodology, we aim to improve the overall data quality. To ensure the accuracy and completeness of the data, we conducted a thorough comparison between the datasets generated by the NegotiateAI2.0 application (available on Hugging Face) and the new NegotiateAI3.0 dataset. This comparison was performed for each session to verify that no data entries were missed during the scraping process. You can find more information in docs/data_quality_checks.

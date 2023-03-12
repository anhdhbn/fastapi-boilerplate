# Fastapi boilerplate

## Installation

Use Docker & Docker Compose

- Clone Project
- Run docker-compose

```
git clone git@github.com:anhdhbn/fastapi-boilerplate.git
cd fastapi-boilerplate
docker-compose build      # build docker image depend on Dockerfile
docker-compose up -d      # auto build docker image depend on Dockerfile & run service
```

## Project structure

```
.
├── app
│   ├── api           // api endpoint
│   ├── core          // contain config of project
│   ├── helpers       // helper functions
│   ├── models        // Contain database model, and alembic for auto generating migration
│   ├── schemas       // Pydantic schemas
│   ├── services      // Contain business logic 
│   ├── repositories  // Contain db queries
│   └── middlewares   // config middleware, handle exception etc
│   └── main.py       // start app here
├── tests
│   ├── api           // contain file tests for each api
│   └── conftest.py   // config for testing
├── .gitignore
├── alembic.ini
├── docker-compose.yaml
├── Dockerfile
├── env.example
├── README.md
└── requirements.txt
```

## Migration

- `alembic revision -m "your message" --autogenerate`   # Create migration versions depend on changed in models
- `alembic upgrade head`   # Upgrade to last version migration
- `alembic downgrade -1`   # Downgrade to before version migration

## Run code

- `pip install -r requirements.txt`
- `uvicorn --host 0.0.0.0 app.main:app --reload --reload-dir=app --port 8000`

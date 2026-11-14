.PHONY: help up down dev-db lint test migrate

help:
	@echo "Targets: up | down | dev-db | lint | test | migrate"

up:
	docker compose up -d

down:
	docker compose down

dev-db:
	docker compose up -d db redis storage

lint:
	cd backend && ruff check . && mypy src
	cd frontend && pnpm lint

test:
	cd backend && pytest -q
	cd frontend && pnpm test

migrate:
	cd backend && alembic upgrade head

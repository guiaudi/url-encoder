.DEFAULT_GOAL := help

APP_NAME = url-encoder
APP_URL = http://localhost:5000

.PHONY: help up down restart logs build open ps

help: ## Show available commands
	@echo ""
	@echo "Available commands:"
	@echo ""
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | \
	awk 'BEGIN {FS = ":.*?## "}; {printf "  %-15s %s\n", $$1, $$2}'
	@echo ""

up: ## Start containers
	docker compose up -d

down: ## Stop containers
	docker compose down

stop: ## Stop containers (without removing)
	docker compose stop

restart: ## Restart containers
	docker compose down
	docker compose up -d

build: ## Build containers
	docker compose build

logs: ## Show container logs
	docker compose logs -f

ps: ## Show running containers
	docker compose ps

open: ## Open app in browser
	@echo "Opening $(APP_URL)..."
	@xdg-open $(APP_URL) 2>/dev/null || open $(APP_URL) 2>/dev/null || echo "Browser already opened or not supported"

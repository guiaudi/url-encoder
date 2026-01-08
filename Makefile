

# ==============================
# Project: URL Encoder
# ==============================

APP_NAME=url-encoder
APP_URL=http://localhost:5000
BROWSER_LOCK=.browser_opened

.DEFAULT_GOAL := help

## ------------------------------
## Core commands
## ------------------------------

## Build the Docker images
build:
	docker compose build

## Start the application
up:
	docker compose up -d

## Stop the application
down:
	docker compose down
	rm -f $(BROWSER_LOCK)

## Restart the application
restart: down up

## View container logs
logs:
	docker compose logs -f

## Open the application in the default browser (only once)
open:
	@if [ ! -f $(BROWSER_LOCK) ]; then \
		echo "Opening browser at $(APP_URL)"; \
		xdg-open $(APP_URL); \
		touch $(BROWSER_LOCK); \
	else \
		echo "Browser already opened"; \
	fi

## Start app and open browser safely
run: up open

## Clean Docker artifacts
clean:
	docker compose down -v --remove-orphans
	docker system prune -f
	rm -f $(BROWSER_LOCK)

## ------------------------------
## Help
## ------------------------------

## Show this help menu
help:
	@echo ""
	@echo "Usage:"
	@echo "  make <command>"
	@echo ""
	@echo "Available commands:"
	@awk 'BEGIN {FS = ":.*##"} \
		/^[a-zA-Z_-]+:.*##/ { \
			printf "  \033[36m%-12s\033[0m %s\n", $$1, $$2 \
		}' $(MAKEFILE_LIST)
	@echo ""


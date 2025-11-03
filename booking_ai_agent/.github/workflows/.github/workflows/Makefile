.PHONY: help build test run clean

help:
	@echo "Available commands:"
	@echo "  build     - Build Docker image"
	@echo "  run       - Run application with docker-compose"
	@echo "  test      - Run tests"
	@echo "  clean     - Clean up Docker resources"
	@echo "  push      - Push to registry"

build:
	docker build -t booking-ai-agent .

run:
	docker-compose up --build

run-detached:
	docker-compose up -d --build

stop:
	docker-compose down

test:
	docker-compose run app pytest backend/tests/ -v

clean:
	docker system prune -f
	docker volume prune -f

logs:
	docker-compose logs -f

push:
	docker push booking-ai-agent:latest
# Variables
DOCKER_REGISTRY=langgenius
API_IMAGE=$(DOCKER_REGISTRY)/higgs-agents-api
VERSION=latest

# Build Docker images
build-api:
	@echo "Building API Docker image: $(API_IMAGE):$(VERSION)..."
	docker build --platform=linux/amd64,linux/arm64 -t $(API_IMAGE):$(VERSION) ./api
	@echo "API Docker image built successfully: $(API_IMAGE):$(VERSION)"

# Push Docker images
push-api:
	@echo "Pushing API Docker image: $(API_IMAGE):$(VERSION)..."
	docker push $(API_IMAGE):$(VERSION)
	@echo "API Docker image pushed successfully: $(API_IMAGE):$(VERSION)"

# Build all images
build-all: build-api

# Push all images
push-all: push-api

build-push-api: build-api push-api

# Build and push all images
build-push-all: build-all push-all
	@echo "All Docker images have been built and pushed."

# Phony targets
.PHONY: build-api push-api build-all push-all build-push-all

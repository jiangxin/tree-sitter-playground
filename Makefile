define message
	@echo "### $(1)"
endef

.PHONY: all
all: format ruff

.PHONY: format
format: isort black

.PHONY: black
black:
	$(call message, Format code using black...)
	@black .

.PHONY: isort
isort:
	$(call message, Format code using isort...)
	@isort  . --interactive

.PHONY: lint ruff
lint: ruff
ruff:
	$(call message, Run lint: ruff check .)
	@python -m ruff check .

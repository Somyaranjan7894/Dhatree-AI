# Contributing to Dhatree AI

First off, thank you for considering contributing to Dhatree AI! It's people like you that make open-source platforms such a great community.

## Development Setup

1. Fork and clone the repository.
2. Set up the backend (Django) inside a virtual environment.
3. Install frontend dependencies using `npm install`.
4. Run `docker-compose up` to start PostgreSQL and Redis.
5. Create a local `.env` from `.env.example`.

## Pull Request Process

1. Ensure any install or build dependencies are removed before the end of the layer when doing a build.
2. Update the README.md with details of changes to the interface, this includes new environment variables, exposed ports, useful file locations and container parameters.
3. You may merge the Pull Request in once you have the sign-off of two other developers, or if you do not have permission to do that, you may request the second reviewer to merge it for you.

## Code Style

- **Python**: We use `ruff` and `black` for formatting.
- **TypeScript/React**: We use `eslint` and `prettier`.

Please ensure all tests pass (`pytest` for backend, `npm test` for frontend) before submitting a PR.

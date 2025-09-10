# Contributing Guide

The following document describes how to contribute to this repository and the
required setup for your development environment.

This repository is generated using [`copier`](https://copier.readthedocs.io).
The [template documentation](https://github.com/remerge/template#readme)
explains how to generate and update this repository from the template.

## Getting Started

The [template repository](https://github.com/remerge/template) provides a
`make`-based development workflow that can be extended and customized per
project.

The [template documentation](https://github.com/remerge/template#readme)
explains the default development workflow and all `make` targets in detail.

To get started quickly clone this repository and use `make install check` to
install project dependencies and ensure that your development environment works.

The following system dependencies are are not managed by this repository and
need to be installed manually.

- [docker](https://www.docker.com/products/docker-desktop/) or access to a
  working docker host
- [pre-commit](https://pre-commit.com) to run formatting and linting
- [direnv](https://direnv.net) to ensure a working environment
- [copier](https://copier.readthedocs.io) to update this repository from the
  template

Most dependencies can be installed using [Homebrew](https://brew.sh):

```shell
brew install docker pre-commit direnv copier
```

Once `pre-commit` hook is activated (`make pre-commit-install`),
set of formatting and linting routines is run automatically on each commit.
The step could be avoided by providing `--no-verify` flag for `git commit`.

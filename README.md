# Clyna Projecta

## Overview

This project consists of both frontend and backend components, with separate development branches for each.

## Getting Started

### Prerequisites

You should have the following programs installed:

- [pip](django)
- [pip] (django)
- [pnpm](https://pnpm.io/)>=9.4.0

### Setup Instructions

1. Clone the repository:

   ```sh
   git clone https://github.com/alx-cohort-4/healthline.git
   cd healthline
   ```

2. Choose your development branch:

   For Frontend Development:

   ```sh
   git checkout frontend
   git pull origin frontend
   pnpm install
   pnpm dev
   ```

   For Backend Development:

   ```sh
   git checkout backend
   git pull origin backend
   ```

### Development Workflow

1. Always create a feature branch from the appropriate base branch:

   ```sh
   git checkout -b your-feature-branch-name
   ```

2. Make your changes and commit them
3. Push your feature branch to origin
4. Create a pull request to the appropriate branch (frontend or backend)

## Important Notes

- Frontend changes must be submitted to the `frontend` branch
- Backend changes must be submitted to the `backend` branch
- Direct pull requests to the `dev` branch are not accepted

## Contributing

For detailed contribution guidelines, please see [CONTRIBUTING](./CONTRIBUTING.md)

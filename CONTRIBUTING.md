# Contribution Guidelines

Welcome to the project! In order to maintain a smooth workflow, please follow the instructions below for setting up your local environment and contributing effectively.

---

## 1. Clone and Setup

When you clone the repository, make sure you follow these steps to ensure you’re working on the correct branch:

1. **Clone the repository** to your local machine:

   ```bash
   git clone https://github.com/alx-cohort-4/healthline.git
   cd healthline
   ```

2. **Frontend Work**:

   - If you’re working on the **frontend**, switch to the **`frontend` branch**:

     ```bash
     git checkout frontend
     ```

   - If you’re working on the **frontend**, make sure to pull the latest changes:
     ```bash
     git pull origin frontend
     ```

   ````
   ```bash
   pnpm install
   pnpm dev
   ````

3. **Backend Work**:

   - If you’re working on the **backend**, switch to the **`backend` branch**:
     ```bash
     git checkout backend
     ```

4. **Pull the Latest Changes** from the origin (this ensures you’re working with the latest version):
   ```bash
   git pull origin <branch_name>
   ```

---

## 2. Create a New Feature Branch

Once you’re on the correct branch (frontend or backend), **create a new feature branch** for the task you’ve been assigned:
make sure to create a new feature branch for each task you are working on. This helps keep the code organized and allows for easier collaboration.

1. Create your feature branch from the **frontend** or **backend** branch:

   ```bash
   git checkout -b <your-feature-branch-name>
   ```

2. Work on your task, make commits, and push your changes to your feature branch:
   ```bash
   git push origin <your-feature-branch-name>
   ```

---

## 3. Pull Request Guidelines

When your task is ready and you’re ready to submit your work:

1. **Do not open a pull request directly to `dev`**.

   - **Backend PRs**: Your PR should be created against the **`backend` branch**.
   - **Frontend PRs**: Your PR should be created against the **`frontend` branch**.

2. Once your PR is created, it will be reviewed by a designated reviewer. After approval, your changes will be merged into the **`dev` branch**.

---

## 4. Important Notes

- **PRs to `dev`**: Any pull request made **directly to the `dev` branch** will be **automatically closed** without review.
- **Emergency Merges**: If you believe your changes need to be merged directly into `dev`, please **contact the reviewer** or **project lead** for explicit permission before proceeding.

---

By following these steps, you’ll be contributing effectively to the project, maintaining a clean workflow, and minimizing conflicts. Thanks for being part of the team!

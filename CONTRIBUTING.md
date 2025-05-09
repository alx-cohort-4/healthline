# Contribution Guidelines

Welcome to the project! In order to maintain a smooth workflow, please follow the instructions below for setting up your local environment and contributing effectively.

---

## 1. Clone and Setup

When you clone the repository, make sure you follow these steps to ensure you're working on the correct branch:

1. **Clone the repository** to your local machine:

   ```bash
   git clone https://github.com/alx-cohort-4/healthline.git
   cd healthline
   ```

2. **Frontend Work**:

   - If you're working on the **frontend**, switch to the **`frontend` branch**:

     ```bash
     git checkout frontend
     ```

   - If you're working on the **frontend**, make sure to pull the latest changes:

     ```bash
     git pull origin frontend
     ```

   ```bash
   pnpm install
   pnpm dev
   ```

3. **Backend Work**:

   - If you're working on the **backend**, switch to the **`backend` branch**:

     ```bash
     git checkout backend
     ```

4. **Pull the Latest Changes** from the origin (this ensures you're working with the latest version):

   ```bash
   git pull origin backend
   ```

---

## 2. Create a New Feature Branch

Once you're on the correct branch (frontend or backend), **create a new feature branch** for the task you've been assigned:
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

### Branch Naming Rules

- You will likely work on features, bug fixes, refactors (restructuring code without changing functionality), chores on the repo (routine tasks such as updating dependencies or changing configurations), or documentation. Each of the type of update should be used as a prefix your branch name as `feat/`, `refactor/`, `fix/`, `chore/`, or `docs/`
- For any of these updates, you will likely use a ticket or an issue. The ticket number, e.g. 001 or issue number should also be included in your branch name
- Finally, a short description for your update should follow suit. This is often taken from the ticket title

> Thus, a typical branch should look like `feat/001-create-login-page` or like `chore/remove-unused-variables` if your update has no corresponding ticket or issue (unlikely)

1. After making changes, add them to the staging area:

   ```bash
   git add .
   ```

2. Commit your changes with a meaningful message:

   ```bash
   git commit -m "feat: your commit message"
   ```

### Commit Message Rules

Commit messages also follow a similar pattern. However, there is no need to add ticket number since they can be easily tracked given the branch name. Instead, use a colon, `:`, after the type of change (`feat`, `fix`, etc.), a whitespace, then your commit message. In cases where you are required to add the ticket number, you may use a the parenthesis after the type of change, like `feat(001): your commit message`

> Another example: `refactor: use a single state for formData` or `refactor(001): use a single state for formData`

> Please notice how both branch names an commit messages use the imperative tense. The imperative tense is a command or request, which makes it clear what the commit does. i.e., "fix login issue", NOT "I fixed login issue", and NOT "fixed login issue"

3. Push your branch to your remote origin branch:

   ```bash
   git push origin <your-branch>
   ```

### Submitting Pull Requests

1. Ensure your branch is up to date with your remote repository:

   ```bash
   git checkout frontend / backend
   git pull origin frontend / backend
   git checkout <your-branch>
   git merge frontend / backend
   ```

> You should regularly update your remote repository with changes from the [default branch of the] upstream repository

2. Run tests and ensure all tests pass:

   ```bash
   pnpm test
   ```

> Make it a habit to run tests before creating pull requests.

3. Submit a pull request from your branch to the upstream repository.
4. In your pull request description, explain what changes you made and why.

## Code of Conduct

This project adheres to the [Contributor Covenant Code of Conduct](https://www.contributor-covenant.org/version/2/0/code_of_conduct/). By participating, you are expected to uphold this code.

## 3. Pull Request Guidelines

When your task is ready and you're ready to submit your work:

1. **Do not open a pull request directly to `dev`**.

   - **Backend PRs**: Your PR should be created against the **`backend` branch**.
   - **Frontend PRs**: Your PR should be created against the **`frontend` branch**.

2. Once your PR is created, it will be reviewed by a designated reviewer. After approval, your changes will be merged into the **`dev` branch**.

---

## 4. Important Notes

- **PRs to `dev`**: Any pull request made **directly to the `dev` branch** will be **automatically closed** without review.
- **Emergency Merges**: If you believe your changes need to be merged directly into `dev`, please **contact the reviewer** or **project lead** for explicit permission before proceeding.

---

By following these steps, you'll be contributing effectively to the project, maintaining a clean workflow, and minimizing conflicts. Thanks for being part of the team!

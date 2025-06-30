# GitHub Setup Instructions

Follow these steps to set up your WhisperAI Transcription Service on GitHub and prepare it for use with Portainer.

## Step 1: Create a New GitHub Repository

1. Go to [GitHub](https://github.com) and sign in to your account
2. Click the "+" icon in the top-right corner and select "New repository"
3. Name your repository (e.g., "whisperai-container")
4. Add a description (optional): "Containerized WhisperAI transcription service"
5. Choose "Public" visibility (or "Private" if you prefer)
6. Do NOT initialize the repository with a README, .gitignore, or license
7. Click "Create repository"

## Step 2: Push Your Local Repository to GitHub

After creating the repository on GitHub, you'll see instructions to push an existing repository. Follow these steps:

```bash
# Add all files to Git
git add .

# Commit the files
git commit -m "Initial commit: WhisperAI container setup"

# Add the GitHub repository as a remote
git remote add origin https://github.com/yourusername/whisperai-container.git

# Push the repository to GitHub
git push -u origin main
```

Replace `yourusername` with your actual GitHub username and `whisperai-container` with the name you chose for your repository.

## Step 3: Setting Up Portainer with GitHub Repository

Once your code is on GitHub, you can easily deploy it using Portainer:

1. In Portainer, go to "Stacks" and click "Add stack"
2. Choose "Repository" as the build method
3. Enter your GitHub repository URL (e.g., `https://github.com/yourusername/whisperai-container.git`)
4. Set the reference name (usually "main" or "master")
5. Set the compose path to "docker-compose.yml"
6. Name your stack (e.g., "whisperai")
7. Click "Deploy the stack"

For more detailed instructions on using Portainer, refer to the PORTAINER.md file.

## Additional Tips

### Creating a Personal Access Token (if needed)

If you're using HTTPS to connect to GitHub and want to avoid entering your password each time:

1. Go to your GitHub account settings
2. Select "Developer settings" > "Personal access tokens" > "Tokens (classic)"
3. Click "Generate new token"
4. Give it a descriptive name and select the "repo" scope
5. Click "Generate token" and copy the token
6. Use this token as your password when pushing to GitHub

### Setting Up SSH Keys (alternative method)

For more secure access:

1. Generate an SSH key pair if you don't have one:
   ```
   ssh-keygen -t ed25519 -C "your_email@example.com"
   ```
2. Add the public key to your GitHub account:
   - Copy the contents of `~/.ssh/id_ed25519.pub`
   - In GitHub, go to Settings > SSH and GPG keys > New SSH key
   - Paste the key and save
3. Update your remote URL to use SSH:
   ```
   git remote set-url origin git@github.com:yourusername/whisperai-container.git
   ```

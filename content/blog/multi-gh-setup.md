---
slug: multi-gh-setup
title: "Two GitHub Accounts, One Laptop: A Clean Isolation Setup"
meta_description: A practical setup for using personal and work GitHub accounts on one machine with deterministic routing for identity, SSH keys, and GitHub CLI sessions.
description: A practical setup for isolating personal and work GitHub contexts so folder path, SSH alias, and CLI wrapper decide account automatically.
pill: GitHub · Workflow
published: "2026"
read_time: "~8 min read"
topics: Git config, SSH, GitHub CLI
toc:
  - id: mental-model
    label: The mental model
  - id: route-git-identity
    label: 1) Route Git identity by folder
  - id: route-ssh-auth
    label: 2) Route SSH auth by host alias
  - id: isolate-gh-cli
    label: 3) Isolate GitHub CLI with zsh wrappers
  - id: alias-based-remotes
    label: 4) Use alias-based remotes in every repo
  - id: daily-workflow
    label: 5) Daily workflow (no account switching)
  - id: troubleshooting
    label: Troubleshooting cheatsheet
  - id: why-this-works
    label: Why this works long-term
---

I wanted one machine to handle both personal and work GitHub without constant account confusion.
This setup solved it by isolating three things:

- Git commit identity (name/email)
- SSH authentication key
- GitHub CLI session (`gh`)

I use fictional accounts in this guide:
- Personal: `alex-dev`
- Work: `acme-engineer`

---

## The mental model {#mental-model}

I stopped thinking in terms of "switching accounts" and started thinking in terms of "context decides account."

- Folder decides Git identity
- Remote host alias decides SSH key
- Command alias (`ghp` vs `ghw`) decides GitHub CLI account

No global toggling needed.

---

## 1) Route Git identity by folder {#route-git-identity}

Choose folder roots:

- `~/Desktop/Dev/personal/`
- `~/Desktop/Dev/work/`

In `~/.gitconfig`:

```ini
[user]
    useConfigOnly = true

[includeIf "gitdir:~/Desktop/Dev/personal/"]
    path = ~/.gitconfig-personal

[includeIf "gitdir:~/Desktop/Dev/work/"]
    path = ~/.gitconfig-work
```

Create `~/.gitconfig-personal`:

```ini
[user]
    name = alex-dev
    email = alex-dev@users.noreply.github.com
```

Create `~/.gitconfig-work`:

```ini
[user]
    name = acme-engineer
    email = alex.chen@acme.com
```

### Verify

Inside a personal repo:

```bash
git config user.name
git config user.email
```

Inside a work repo:

```bash
git config user.name
git config user.email
```

Expected: personal repo returns personal identity; work repo returns work identity.

---

## 2) Route SSH auth by host alias {#route-ssh-auth}

Goal: give each account its own SSH identity path, then map it with host aliases.

### Setup pattern (works for both work and personal)

For each account, choose one:
- **Reuse existing key** if that key is already in the correct GitHub account
- **Create a new key** if no key exists yet

Where to check existing keys:
- GitHub -> **Settings -> SSH and GPG keys**

How to confirm a local key matches GitHub:

```bash
ssh-keygen -lf ~/.ssh/id_rsa.pub
ssh-keygen -lf ~/.ssh/id_ed25519_github_personal.pub
```

Compare SHA256 fingerprints from terminal with what GitHub shows.

### Example: work account

If reusing existing key:
- Keep using `~/.ssh/id_rsa` (or your current work key path)

If creating a new key:

```bash
ssh-keygen -t ed25519 -C "alex.chen@acme.com" -f ~/.ssh/id_ed25519_github_work
ssh-add --apple-use-keychain ~/.ssh/id_ed25519_github_work
```

Add the matching `.pub` key to the **work** GitHub account in
**Settings -> SSH and GPG keys -> New SSH key** (key type: Authentication Key).

### Example: personal account

If creating a new key:

```bash
ssh-keygen -t ed25519 -C "alex-dev@users.noreply.github.com" -f ~/.ssh/id_ed25519_github_personal
ssh-add --apple-use-keychain ~/.ssh/id_ed25519_github_personal
```

Then add `~/.ssh/id_ed25519_github_personal.pub` to the **personal** GitHub account.

In `~/.ssh/config`:

```sshconfig
Host *
  AddKeysToAgent yes
  UseKeychain yes

Host github-work
  HostName github.com
  User git
  # Use one of the following:
  # IdentityFile ~/.ssh/id_rsa
  # IdentityFile ~/.ssh/id_ed25519_github_work
  IdentityFile ~/.ssh/id_rsa
  IdentitiesOnly yes

Host github-personal
  HostName github.com
  User git
  IdentityFile ~/.ssh/id_ed25519_github_personal
  IdentitiesOnly yes
```

Repeat the same pattern for the other account: reuse if already present, otherwise create and add.

### Verify

```bash
ssh -T github-work
ssh -T github-personal
```

Expected:
- Work alias authenticates as work account
- Personal alias authenticates as personal account

---

## 3) Isolate GitHub CLI with zsh wrappers {#isolate-gh-cli}

By default, `gh` keeps one active account per host.
So I created two wrappers that use separate config directories.

Add to `~/.zshrc`:

```bash
ghp() { GH_CONFIG_DIR="$HOME/.config/gh-personal" gh "$@"; }
ghw() { GH_CONFIG_DIR="$HOME/.config/gh-work" gh "$@"; }
```

Reload shell:

```bash
source ~/.zshrc
```

Login once per profile:

```bash
ghp auth login --hostname github.com --git-protocol ssh
ghw auth login --hostname github.com --git-protocol ssh
```

### Verify

```bash
ghp auth status -h github.com
ghw auth status -h github.com
```

Expected:
- `ghp` shows personal user
- `ghw` shows work user

---

## 4) Use alias-based remotes in every repo {#alias-based-remotes}

This is the final lock that keeps things deterministic.

- Personal repo remote format:
  - `git@github-personal:alex-dev/repo-name.git`
- Work repo remote format:
  - `git@github-work:acme-org/repo-name.git`

Set or fix origin:

```bash
git remote set-url origin git@github-personal:alex-dev/repo-name.git
# or
git remote set-url origin git@github-work:acme-org/repo-name.git
```

### Verify

```bash
git remote -v
```

Expected: remote uses `github-personal` or `github-work`, not plain `github.com`.

---

## 5) Daily workflow (no account switching) {#daily-workflow}

- Keep personal repos in `~/Desktop/Dev/personal/...`.
- Keep work repos in `~/Desktop/Dev/work/...`.
- Use `git push` normally.
- Use `ghp ...` for personal GitHub CLI actions.
- Use `ghw ...` for work GitHub CLI actions.

Quick pre-push sanity check:

```bash
git config user.name
git config user.email
git remote -v
```

---

## Troubleshooting cheatsheet {#troubleshooting}

- **`Permission denied (publickey)`**
  - Wrong key on account, or wrong host alias in remote.
  - Check `~/.ssh/config`, then run `ssh -T github-work` / `ssh -T github-personal`.

- **Wrong commit identity**
  - Repo not under your include path, or include file has wrong values.
  - Check `git config --show-origin --get user.name`.
  - Confirm you are inside a Git repo with `git rev-parse --is-inside-work-tree`.

- **`gh` shows wrong account**
  - You used plain `gh` instead of wrapper.
  - Use `ghp` or `ghw`, then `... auth status -h github.com`.

---

## Why this works long-term {#why-this-works}

This setup removes memory-based switching and replaces it with structure-based routing:
- path -> identity
- remote alias -> SSH key
- wrapper command -> GitHub CLI profile

That is what makes it reliable months later, including for "future me."

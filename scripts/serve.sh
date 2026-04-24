#!/usr/bin/env bash
# Run from the repo root or from scripts/ — both work.
set -euo pipefail

REPO_ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"

# ── Helpers ────────────────────────────────────────────────────────────────────

red()   { printf '\033[0;31m%s\033[0m\n' "$*"; }
green() { printf '\033[0;32m%s\033[0m\n' "$*"; }
blue()  { printf '\033[0;34m%s\033[0m\n' "$*"; }
bold()  { printf '\033[1m%s\033[0m\n' "$*"; }

require_sudo() {
    local reason="$1"
    bold ""
    bold "── sudo required ────────────────────────────────────────────────────"
    blue "  Why: $reason"
    bold "─────────────────────────────────────────────────────────────────────"
    echo ""
    sudo -v   # cache credentials; subsequent sudo calls within this script reuse them
}

# ── 1. Ruby ────────────────────────────────────────────────────────────────────

blue "Checking Ruby..."
if ! command -v ruby &>/dev/null; then
    require_sudo "Ruby is not installed. Installing via apt requires root privileges."
    sudo apt-get update -qq
    sudo apt-get install -y ruby-full build-essential zlib1g-dev
    green "  Ruby installed: $(ruby --version)"
else
    green "  Ruby found: $(ruby --version)"
fi

# ── 2. Build dependencies for native gems ──────────────────────────────────────

blue "Checking build tools (gcc, make, zlib, ruby-dev)..."
MISSING_PKGS=()
for pkg in build-essential zlib1g-dev ruby-dev; do
    dpkg -s "$pkg" &>/dev/null 2>&1 || MISSING_PKGS+=("$pkg")
done

if [[ ${#MISSING_PKGS[@]} -gt 0 ]]; then
    require_sudo "Missing packages: ${MISSING_PKGS[*]}. Jekyll gems compile C extensions and need Ruby header files (ruby.h) and a C toolchain."
    sudo apt-get update -qq
    sudo apt-get install -y "${MISSING_PKGS[@]}"
    green "  Installed: ${MISSING_PKGS[*]}"
else
    green "  Build tools present (build-essential, zlib1g-dev, ruby-dev)."
fi

# ── 3. Bundler ─────────────────────────────────────────────────────────────────

blue "Checking Bundler..."
if ! command -v bundle &>/dev/null; then
    # Install bundler into the user gem directory — no sudo needed
    echo "  Installing Bundler (user gem, no sudo)..."
    gem install bundler --user-install
    # Make sure user gem bin is on PATH for the rest of this session
    USER_GEM_BIN="$(ruby -e 'puts Gem.user_dir')/bin"
    export PATH="$USER_GEM_BIN:$PATH"
    green "  Bundler installed: $(bundle --version)"
else
    green "  Bundler found: $(bundle --version)"
fi

# ── 4. Gem dependencies ────────────────────────────────────────────────────────

blue "Installing gem dependencies from Gemfile..."
cd "$REPO_ROOT"

# Install gems into vendor/bundle inside the repo so nothing touches system Ruby
bundle config set --local path 'vendor/bundle' 2>/dev/null || true

if ! bundle check &>/dev/null 2>&1; then
    bundle install
    green "  Gems installed."
else
    green "  Gems already up to date."
fi

# ── 5. Serve ───────────────────────────────────────────────────────────────────

bold ""
bold "Starting Jekyll development server..."
blue "  URL:  http://localhost:4000"
blue "  Stop: Ctrl+C"
echo ""

bundle exec jekyll serve --livereload --baseurl ""

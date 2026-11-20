# ===========================================
# Git Operations
# ===========================================

# Commit changes to dev branch
commit:
	$(eval msg ?= $(filter-out $@,$(MAKECMDGOALS)))
	@if "$(msg)"=="" (echo Please provide a commit message: make commit "your message" & exit 1)
	git status
	git add .
	git status
	git commit -m "$(msg)"
	git push origin

%:
	@:

# Sync local branch with remote (defaults to dev branch)
sync:
	$(eval branch ?= dev)
	git fetch origin
	git checkout $(branch)
	git pull origin $(branch)

# Propagate AGENTS.md and .agents/ to every sibling Blender add-on
sync_agents:
	powershell -NoProfile -ExecutionPolicy Bypass -File sync_agents.ps1

# Build project with Blender's extension build (override BLENDER to pick a binary)
BLENDER ?= $(shell python -c "import glob, os, shutil; root=os.path.expanduser('~/Downloads/Blender/stable'); found=sorted(glob.glob(os.path.join(root,'blender-5*','blender.exe')) or glob.glob(os.path.join(root,'blender-5*','blender'))); print(shutil.which('blender') or found[-1])")
build: get_version
	$(eval ROOT_DIR := $(notdir $(CURDIR)))
	python -c "import os; os.makedirs('releases', exist_ok=True)"
	$(BLENDER) --command extension build --source-dir . --output-filepath releases/$(ROOT_DIR)_v$(VERSION).zip
	@echo "Successfully built the release zip"

# ===========================================
# Pull Request Management
# ===========================================

# Get version from TOML file (stdlib tomllib, Python 3.11+)
get_version:
	@echo "Extracting version from blender_manifest.toml..."
	$(eval VERSION := $(shell python -c "import tomllib; print(tomllib.load(open('blender_manifest.toml','rb'))['version'])" 2>nul))
	@if "$(VERSION)"=="" (echo ERROR: Failed to extract version from blender_manifest.toml & exit 1)
	@echo "Version extracted: $(VERSION)"

# Create PR from dev to main
create_pr: get_version
	gh pr create --base main --head dev --title "Version $(VERSION)" --body-file CHANGELOG.md

# Merge PR automatically
merge_pr: get_version
	gh pr merge --auto --merge
	@echo "Successfully merged dev into main"

# ===========================================
# Release Management
# ===========================================

# Create GitHub release with version tag and release assets
create_release: get_version
	$(eval ROOT_DIR := $(notdir $(CURDIR)))
	@echo "Creating release with version: $(VERSION)"
	gh release create "v$(VERSION)" --target main --title "Version $(VERSION)" --notes-file CHANGELOG.md releases/$(ROOT_DIR)_v$(VERSION).zip

# ===========================================
# Complete Release Workflow
# ===========================================

# Execute full release process: sync, build, PR creation/merge, and release
release: sync build create_pr merge_pr create_release
	@echo "Successfully created release"
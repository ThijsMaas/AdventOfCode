git filter-branch --tree-filter "rm -rf data" --prune-empty HEAD
git for-each-ref --format="%(refname)" refs/original/ | xargs -n 1 git update-ref -d
git add .gitignore
git commit -m 'Removing data from git history'
git gc
git push origin main --force
# 1. 添加 upstream（原项目地址）
git remote add upstream https://github.com/openai/codex.git

# 2. 验证一下
git remote -v

git fetch upstream
git checkout main
git merge upstream/main
git add .
git commit -m "Merge upstream/main into main"
git push origin main


git rm --cached codex-py/lib/_416_coder/codex
git status
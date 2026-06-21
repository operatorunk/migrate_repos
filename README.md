# migrate_repos
repository to add repositories report scripts

# 1. Clonar desde el mirror local si ya lo tienes
git clone <repo>.git <repo>-clean
cd <repo>-clean

# 2. Asegurar rama master
git checkout master
git status

# 3. Borrar histórico Git
rm -rf .git

# 4. Crear repo limpio
git init
git add .
git commit -m "Initial clean migration from Bitbucket master"
git branch -M master

# 5. Añadir Azure como remoto
git remote add origin https://dev.azure.com/ORG/PROJECT/_git/migrated-PROJECT_KEY-repo_slug

# 6. Reducir compresión si quieres evitar bloqueos
git config core.compression 0

# 7. Subir a Azure
git push -u origin master

# 8. Validar
git log --oneline --decorate -5
git remote -v

Si no tienes mirror local y quieres clonar directo desde Bitbucket:

git clone https://bitbucket.tuempresa.com/scm/PROJECT_KEY/repo_slug.git <repo>-clean
cd <repo>-clean
git checkout master
rm -rf .git
git init
git add .
git commit -m "Initial clean migration from Bitbucket master"
git branch -M master
git remote add origin https://dev.azure.com/ORG/PROJECT/_git/migrated-PROJECT_KEY-repo_slug
git config core.compression 0
git push -u origin master

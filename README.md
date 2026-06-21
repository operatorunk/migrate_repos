# migrate_repos
repository to add repositories report scripts

# Paso 1: clonar en mirror

En una carpeta nueva:

git clone --mirror https://bitbucket.tuempresa.com/scm/PROJECT_KEY/repo_slug.git

Entra en el mirror:

cd repo_slug.git

# Paso 2: comprobar tamaño antes de subir
git count-objects -vH

Mira este valor:

size-pack

Si size-pack es menor de 5 GB, probamos migración completa.

# Paso 3: apuntar a Azure
git remote set-url origin https://dev.azure.com/ORG/PROJECT/_git/migrated-PROJECT_KEY-repo_slug

Comprueba:

git remote -v

# Paso 4: push completo
git push --mirror origin

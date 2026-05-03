# Pasos en PowerShell: primer push + submódulo Numina

Úsalo si ves errores como:

- `error: 'lean_project/' does not have a commit checked out`
- `Author identity unknown`
- `src refspec main does not match any` (porque el commit falló antes)

Los mensajes `LF will be replaced by CRLF` son **avisos normales en Windows**, no son errores.

---

## Paso A — Quién sos en Git (obligatorio una vez)

Sustituí por tu nombre real y el email de tu cuenta GitHub:

```powershell
git config --global user.name "Ayrton Porto"
git config --global user.email "tu-email-usado-en-github@ejemplo.com"
```

---

## Paso B — Quitar el `.git` **dentro** de `lean_project` (arregla el error del commit)

Tu carpeta `lean_project` tiene **su propio** `.git` (repo Git anidado). El repo padre no puede “meterla entera” como carpeta normal hasta que eso no moleste.

**AViD usa `lean_project` como parte del mismo repo** (no como submódulo), así que lo habitual es **eliminar solo** ese `.git` interno. Tus archivos `.lean`, `lakefile.toml`, etc. **no se borran**.

```powershell
cd "D:\Mis documentos\Documentos\AViD Journal"

# Copia de seguridad por si acaso (opcional)
# Copy-Item -Recurse "lean_project" "lean_project_backup_sin_git"

Remove-Item -Recurse -Force ".\lean_project\.git"
```

Si `Remove-Item` dice que no existe, ya está bien; pasá al siguiente paso.

---

## Paso C — Primer commit del repo (sin submódulo todavía)

Así evitás errores raros de `git submodule add` si Git pide historial previo.

```powershell
cd "D:\Mis documentos\Documentos\AViD Journal"

git add -A
git status
git commit -m "Initial commit: AViD Journal"
git branch -M main
```

Todavía **no** hagas `git push` si querés meter el submódulo en el mismo “primer push”: seguí al paso D y después E.

---

## Paso D — Numina como **submódulo**

La carpeta `Numina Lean Agent/` está en `.gitignore` (copia local); **no se sube**.

El oficial queda en:

`vendor/numina-lean-agent` → https://github.com/project-numina/numina-lean-agent

```powershell
cd "D:\Mis documentos\Documentos\AViD Journal"

git submodule add https://github.com/project-numina/numina-lean-agent.git vendor/numina-lean-agent

git add .gitmodules vendor/numina-lean-agent
git commit -m "Add Numina Lean Agent as submodule"
```

**Clonar tu repo con Numina incluido:**

```powershell
git clone --recurse-submodules https://github.com/ayrtonporto/avid-journal.git
```

Si ya clonaron sin `--recurse-submodules`:

```powershell
git submodule update --init --recursive
```

---

## Paso E — Push a GitHub

```powershell
git push -u origin main
```

Si **GitHub ya tiene commits** (ej. README al crear el repo):

```powershell
git pull origin main --allow-unrelated-histories
git add -A
git commit -m "Merge remote main"
git push -u origin main
```

---

## Paso F — Autenticación en push

Si pide usuario/contraseña: en GitHub usá un **Personal Access Token** como contraseña, o instalá **GitHub CLI** y ejecutá `gh auth login`.

---

## Resumen

| Problema | Qué hacer |
|----------|-----------|
| `lean_project/` … commit checked out | Borrar `lean_project\.git` |
| Author unknown | `git config --global user.name` / `user.email` |
| LF/CRLF | Ignorar o `git config core.autocrlf true` |
| Numina duplicada | Carpeta ignorada + submódulo en `vendor/numina-lean-agent` |

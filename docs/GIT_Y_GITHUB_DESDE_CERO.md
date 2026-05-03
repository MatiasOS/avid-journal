# Git y GitHub desde cero (para AViD Journal)

Esta guía asume que **no has usado Git/GitHub antes**, que **ya creaste el repositorio vacío en GitHub**, que **solo tú escribes código**, y que quieres **no duplicar** código que ya está en otros repos (Numina, Mathlib).

---

## 1. Dos herramientas distintas


| Qué es     | Para qué sirve                                                                                                                  |
| ---------- | ------------------------------------------------------------------------------------------------------------------------------- |
| **Git**    | Programa en tu PC: guarda **historial de versiones** (commits), ramas, etc. Funciona **sin internet** para trabajar localmente. |
| **GitHub** | Sitio web donde **guardas una copia** de ese historial y lo compartes. Ahí otros clonan, ves issues, etc.                       |


Metáfora: Git es el cuaderno de borrador con todas las versiones; GitHub es la fotocopia oficial que dejas en la biblioteca.

---

## 2. Instalar Git en Windows

1. Descarga **Git for Windows**: [https://git-scm.com/download/win](https://git-scm.com/download/win)
2. Instala con opciones por defecto (incluye **Git Bash**, útil).
3. Abre **PowerShell** o **Git Bash** en tu carpeta del proyecto:
  ```powershell
   cd "D:\Mis documentos\Documentos\AViD Journal"
  ```
4. Di quién eres (una sola vez por PC):
  ```powershell
   git config --global user.name "Tu Nombre"
   git config --global user.email "tu.email@ejemplo.com"
  ```
   El email puede ser el mismo que usas en GitHub (si tu cuenta lo muestra).

---

## 3. Conceptos mínimos (los tres “cajones”)

1. **Working tree** — Carpetas y archivos que ves y editas.
2. **Staging (`git add`)** — Marcas **qué cambios** van a formar parte del próximo “foto” (commit).
3. **Commit** — Una **foto** del proyecto con mensaje (“Initial commit”, etc.).
4. **Push** — Subes esos commits a **GitHub** (`origin`).

Flujo habitual:

```text
editas archivos → git add → git commit → git push
```

---

## 4. Enlazar tu carpeta local con el repo que ya existe en GitHub

Tu caso: **ya tienes** la carpeta con código y **ya existe** el repo en GitHub (vacío o con un README).

### Opción A — Carpeta local **todavía sin historial Git** (`git status` dice “not a git repository`)

```powershell
cd "D:\Mis documentos\Documentos\AViD Journal"
git init
git branch -M main
git remote add origin https://github.com/TU_USUARIO/TU_REPO.git
git add -A
git commit -m "Initial commit"
git push -u origin main
```

La primera vez `git push` puede pedirte iniciar sesión en GitHub (navegador o token).

### Opción B — Ya hiciste `git init` pero **no hay commits** (tu caso anterior)

Igual que arriba desde `git remote add` (si no lo tienes):

```powershell
git remote -v
```

Si **no** sale nada, agrega:

```powershell
git remote add origin https://github.com/TU_USUARIO/TU_REPO.git
```

Luego:

```powershell
git add -A
git status
git commit -m "Initial commit"
git push -u origin main
```

### Opción C — GitHub creó el repo **con** README y te da error al push

GitHub tiene commits que tu PC no tiene. Haz:

```powershell
git pull origin main --allow-unrelated-histories
```

Resuelve conflictos si aparecen (editas archivos, `git add`, `git commit`), y después:

```powershell
git push -u origin main
```

---

## 5. Mathlib: **no lo subas** — ya está “llamado” por Lake

**Mathlib no va dentro de tu repositorio como carpeta gigante.**

En `lean_project/lakefile.toml` ya está declarado algo equivalente a:

- “Descarga Mathlib de la comunidad Lean en la versión `v4.29.0`”.

Cuando alguien clona **tu** repo y ejecuta:

```powershell
cd lean_project
lake update
lake build
```

Lake **descarga y construye** Mathlib en `lean_project/.lake/` (local en cada máquina).

Por eso en `.gitignore` está `**.lake/`**: nadie sube esa carpeta a GitHub.

**Resumen:** Para Mathlib no hace falta submódulo ni copiar código; solo **mantener `lakefile.toml` y `lean-toolchain`** en el repo.

---

## 6. Numina Lean Agent: usar el **repo oficial** en lugar de copiar la carpeta

Tú tienes una carpeta tipo `Numina Lean Agent/` que es un **clon o copia** del proyecto Numina. Lo limpio es:

- **No versionar** esa carpeta entera como archivos sueltos dentro de AViD, **o**
- Usar un **submódulo de Git**: dentro de tu repo guardas solo **la dirección y el commit** del repo oficial.

Repo público que menciona el propio README de Numina (nombre puede variar; comprueba en GitHub):

- [https://github.com/project-numina/numina-lean-agent](https://github.com/project-numina/numina-lean-agent)

### Pasos recomendados (submódulo)

1. **Haz backup** de tu carpeta actual si tenías cambios locales dentro de Numina:
  ```powershell
   Copy-Item -Recurse "Numina Lean Agent" "Numina Lean Agent_backup"
  ```
2. **Quita** la carpeta antigua del índice de Git (cuando ya uses Git), o bórrala del disco **después** de comprobar que no necesitas nada único ahí.
3. Añade el submódulo (ejemplo: carpeta `vendor/numina-lean-agent`):
  ```powershell
   git submodule add https://github.com/project-numina/numina-lean-agent.git vendor/numina-lean-agent
   git commit -m "Add Numina Lean Agent as submodule"
   git push
  ```
4. Quien **clone** tu repo después debe hacer:
  ```powershell
   git clone --recurse-submodules https://github.com/TU_USUARIO/TU_REPO.git
  ```
   O si ya clonó sin submódulos:

### Si prefieres no usar submódulos

- Pon `**Numina Lean Agent/**` en `.gitignore`.
- En el README escribe: “Clonar Numina aparte: `git clone https://github.com/project-numina/numina-lean-agent`”.

Eso también evita duplicar historial; cada uno tiene dos carpetas vecinas.

### Nota sobre AViD

Gran parte del pipeline ya está en `src/formalization/scripts/` (inspirado en Numina). Si **no** necesitas la carpeta Numina para nada en tu día a día, puedes **no** subirla y solo documentar el enlace al proyecto original por reconocimiento.

---

## 7. Resumen de lo que **sí** suele subirse en AViD


| Sube                                                                                     | No subas (local / regenerable)      |
| ---------------------------------------------------------------------------------------- | ----------------------------------- |
| `src/`, `prompts/`, `examples/`, `docs/`, `tests/`                                       | `.venv/`, `.env` con secretos       |
| `lean_project/lakefile.toml`, `lean-toolchain`, `LeanProject/`, `Papers/**/*.lean`, etc. | `lean_project/.lake/`               |
| `.gitignore`, `requirements.txt`, `README.md`                                            | `*.log`, `.claude/` si es solo tuyo |


---

## 8. Próximos días: comando típico

```powershell
cd "D:\Mis documentos\Documentos\AViD Journal"
git status
git add -A
git commit -m "Descripción corta del cambio"
git push
```

---

## 9. Autenticación con GitHub

GitHub **no** acepta tu contraseña de la web en `git push`. Opciones habituales:

- **Git Credential Manager** (suele instalarse con Git for Windows): te abre el navegador.
- **Personal Access Token**: GitHub → Settings → Developer settings → Tokens; lo pegas cuando Git pide “password”.
- **GitHub CLI** (`gh auth login`).

Si algo falla, copia el mensaje de error completo y búscalo tal cual; casi siempre es tema de login.

---

Guía paso a paso en PowerShell (errores típicos + submódulo Numina): **[PASOS_PUSH_WINDOWS.md](PASOS_PUSH_WINDOWS.md)**

---


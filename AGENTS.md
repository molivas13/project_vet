# AGENTS.md

## Project

Django 6 veterinary clinic app ("Pet Lovers", Nicaragua). Single project package `config` + single app `core`. No monorepo, no CI, no linter/typechecker, no requirements file — Django is installed globally.

- Locale: `es-us`, timezone `America/Managua`, currency Córdobas (`C$`). Domain language is Spanish: keep model fields, choices, templates, and messages in Spanish.
- Python: use the `py` launcher (`py manage.py ...`). `python` is NOT on PATH on this machine.

## Commands

```sh
py manage.py runserver        # dev server
py manage.py check            # fastest smoke test — run after any model/url/view change
py manage.py makemigrations   # after model changes
py manage.py migrate
py manage.py test             # no tests exist yet (core/tests.py is empty)
```

No lint/format/typecheck commands exist. Verification order when changing code: `check` -> `makemigrations --check` -> `test`.

## Architecture

- `config/` — settings, root URLconf, WSGI/ASGI. `config/urls.py` mounts admin + `include('core.urls')` at site root.
- `core/` — everything else: models, views, urls (`app_name = "core"`), templates in `core/templates/core/`, static in `core/static/`.
- Domain model (`core/models.py`):
  - `Sucursal` (branch) -> `Farmaco`, `Servicio`, `Cita`
  - `Propietario` -> `Mascota` -> `Cita`; owner link field is `Mascota.propietario` (NOT `dueno`)
  - `CitaFarmaco` is the through-table for `Cita.farmacos_utilizados` (M2M)
- Custom user: `AUTH_USER_MODEL = 'core.User'` (adds `rol`: ADMIN/VET/REP/OWNER). This is already baked into applied migrations and the committed `db.sqlite3` — do not attempt to change or un-set it.
- `Cita.veterinario` has `limit_choices_to={"rol": "VET"}` — enforce that in forms/views too, it's not automatic.

## Conventions & quirks

- FK field `Farmaco.Sucursal` is capitalized (unlike `Servicio.sucursal` / `Cita.sucursal`). Templates and code must use `farmaco.Sucursal` / `farmaco.Sucursal__nombre`. `Farmaco.__str__` currently uses lowercase `self.sucursal` and will raise AttributeError — fix rather than copy the pattern.
- Status vocab: `Cita.ESTADOS` uses `pendiente/programada/atendida/cancelada` and `Cita.TIPOS` uses `consulta/vacunacion/...`. There is no `"confirmada"` state.
- Money is `Decimal` (`Servicio.precio`), displayed as `C$`.
- Templates extend `core/base.html`; static files served from `core/static/` (note: `STATICFILES_DIRS` points at a nonexistent root `static/` — expect a W004 warning; don't create a second static tree without fixing settings).

## Owner ↔ User association (important)

There is NO FK between `core.User` and `Propietario`. All "mis mascotas/mis citas"
queries join via email: `propietario__correo__iexact=user.email` (helpers
`mascotas_del()` / `citas_del()` in `core/views.py`). If you register a propietario,
its `correo` must match the user's email or the panel shows empty lists. A real
FK would be the better long-term fix — if you add one, migrate all these filters.

- `core/forms.py`: `RegistroForm` (saves `rol="OWNER"`) and `CitaForm` (filters
  `veterinario` queryset to `rol="VET"` — keep doing that, `limit_choices_to`
  is not enforced by forms by itself).
- `LOGIN_URL = 'core:login'` / `LOGIN_REDIRECT_URL = 'core:panel'` in settings —
  required because routes live at `/login/`, not Django's default `/accounts/login/`.
- Every URL name must be used namespaced in templates: `{% url 'core:...' %}`
  (app_name = "core").

## Repo hygiene

- `.gitignore` only covers `.env` and `venv/`. `db.sqlite3` and all `__pycache__/*.pyc` files are TRACKED in git. Avoid committing more pyc noise; don't delete tracked files as a "fix" without asking.
- `db.sqlite3` is a committed dev database with migrations applied — useful for local runs, treat it as disposable but don't silently regenerate it.

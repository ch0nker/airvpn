# Contributing

Thanks for your interest in contributing to AirVPN! To keep the library consistent and reliable, please follow the guidelines below before opening a pull request.

## Requirements for new additions

Any new addition — a new method, service, or exception — needs to include:

- **A test function.** New behavior should be covered by a corresponding test. See [tests](tests.md) for how the test suite is structured and how to run it locally.
- **Proper documentation.** Public methods, classes, and exceptions should have complete docstrings (see the existing services for the expected format: `Args`, `Returns`, and `Raises` sections where applicable). You don't need to manually add a page under `docs/` for a new module or class — `gen_pages.py` walks the `airvpn` package on build and generates an `mkdocstrings` page for every submodule and package (via each `__init__.py`) automatically, mirroring the package's folder structure. As long as your addition lives inside the `airvpn` package and has a docstring, it'll show up in the nav on its own.

Pull requests that add functionality without either of these will be asked for changes before merging.

## Documentation generation

A quick note on how the docs site is built, since it affects how your additions will appear:

- Every file and folder inside `airvpn/` gets its own generated page (`<name>.md`) titled after the module, with an `mkdocstrings` `::: module.path` directive pulling in your docstrings. Folders (packages) get an `index.md` generated from their `__init__.py`.
- The page title defaults to the module's name, snake_case-split into words and capitalized (e.g. `dns_lists` → "Dns lists"). If you want a specific display name instead, set `__title__ = "..."` in the module — the generator will use that if present. Note that `__title__` only affects the **nav label and page heading**; it doesn't change the `::: module.path` reference shown under the heading, so the module's actual dotted path is still visible on the page regardless.
- Guide pages under `docs/guides/` are picked up the same way and added under the "Guides" nav section, with `docs/guides/index.md` becoming the "Guides" landing page itself rather than a nested entry. Guide filenames also have underscores converted to spaces for the nav title (e.g. `getting_started.md` → "Getting started"), matching the module title behavior.
- **Module-level docstrings matter, not just class/method ones.** Because each generated page uses `::: module.path` (an `mkdocstrings` directive that renders everything in that module), any docstring placed at the top of the file — before your imports/classes — will be rendered on the page too, typically as introductory text above the class/function documentation. If you're adding a new module, consider adding a short module docstring describing its purpose; it'll show up on the generated page for free and gives readers context before they hit the API reference.

If you add a new top-level guide or module, you shouldn't need to touch `gen_pages.py` or `summary.md` at all — just make sure the file lands in the right place (`airvpn/` for code, `docs/guides/` for guides) with a proper docstring or content.

## Workflow

1. Fork the repository and create a branch for your change.
2. Make your changes, including a test function and documentation as described above.
3. Run the test suite locally to confirm everything passes — see [tests](tests.md) for instructions.
4. Open a pull request describing what changed and why.

## Style

- Follow the existing code style and docstring conventions already used throughout the codebase.
- Keep exceptions consistent with the existing hierarchy (see [exceptions.md](../airvpn/exceptions.md)) — prefer raising a specific, well-documented exception over a generic one.
- Prefer small, focused pull requests over large ones covering multiple unrelated changes.

## Naming conventions

To keep the codebase predictable, please follow the conventions already established:

- **Classes** use `PascalCase` (e.g. `Devices`, `Generator`, `ConfigList`).
- **Methods, functions, and variables** use `snake_case` (e.g. `create_config`, `send_notification`, `output_dir`).
- **Enums** use `PascalCase` for the class and `UPPER_CASE` for members (e.g. `DeviceAction.LIST`, `DeviceAction.ADD`).
- **Exceptions**:
  - Base exceptions for a subsystem end in `Exception` (e.g. `DeviceException`, `GeneratorException`), and should subclass `AirVPNException`.
  - Specific exceptions end in `Error` and describe the failure, not the subsystem twice — `DeviceAPIError`, not `DeviceAPIException` (e.g. `DeviceAPIError`, `GeneratorResponseError`).
  - Prefix specific exceptions with the subsystem they belong to, so it's clear which base exception they fall under at a glance.
- **Private/internal attributes and methods** are prefixed with a single underscore (e.g. `_diff`, `_cache_devices`, `_create_config`), consistent with the rest of the codebase.
- **Files and modules** use `snake_case` matching their primary export where practical (e.g. `models.py`, `exceptions.py`). Since module/page titles are auto-generated from the filename (see "Documentation generation" above), avoid overly abbreviated or ambiguous names — or set `__title__` if the auto-generated title wouldn't read well.

If you're adding something that doesn't cleanly fit an existing pattern, match the convention of the nearest analogous class or exception rather than introducing a new one.

If you're unsure whether a change fits the scope of the project, feel free to open an issue first to discuss it before submitting a pull request.
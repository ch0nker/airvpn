# Contributing

Thanks for your interest in contributing to AirVPN! To keep the library consistent and reliable, please follow the guidelines below before opening a pull request.

## Requirements for new additions

Any new addition — a new method, service, or exception — needs to include:

- **A test function.** New behavior should be covered by a corresponding test. See [tests/README.md](../tests/README.md) for how the test suite is structured and how to run it locally.
- **Proper documentation.** Public methods, classes, and exceptions should have complete docstrings (see the existing services for the expected format: `Args`, `Returns`, and `Raises` sections where applicable), and any user-facing addition should be reflected in the relevant page under `docs/` (or a new page added to [api/README.md](api/README.md) if it introduces a new service).

Pull requests that add functionality without either of these will be asked for changes before merging.

## Workflow

1. Fork the repository and create a branch for your change.
2. Make your changes, including a test function and documentation as described above.
3. Run the test suite locally to confirm everything passes — see [tests/README.md](../tests/README.md) for instructions.
4. Open a pull request describing what changed and why.

## Style

- Follow the existing code style and docstring conventions already used throughout the codebase.
- Keep exceptions consistent with the existing hierarchy (see [api/exceptions.md](api/exceptions.md)) — prefer raising a specific, well-documented exception over a generic one.
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
- **Files and modules** use `snake_case` matching their primary export where practical (e.g. `models.py`, `exceptions.py`).

If you're adding something that doesn't cleanly fit an existing pattern, match the convention of the nearest analogous class or exception rather than introducing a new one.

If you're unsure whether a change fits the scope of the project, feel free to open an issue first to discuss it before submitting a pull request.
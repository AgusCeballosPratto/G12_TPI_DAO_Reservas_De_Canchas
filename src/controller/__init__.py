"""Controller package initializer.

This file makes `src/controller` an explicit Python package so language
servers (like Pylance) and imports such as
`from controller.controlador_reservas import ControladorReservas`
resolve reliably.

Keep this file minimal to avoid side effects when importing the package.
"""

# Expose commonly used controller classes at package level (optional)
try:
    from .controlador_reservas import ControladorReservas  # noqa: F401
except Exception:
    # If import fails during static analysis or partial installs, ignore.
    pass

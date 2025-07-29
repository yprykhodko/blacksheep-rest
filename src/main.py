from blacksheep import Application
from blacksheep.server.diagnostics import get_diagnostic_app
from rodi import Container

from src.core.documentation import docs
from src.core.errors import configure_error_handlers
from src.core.services import configure_services
from src.core.settings import Settings


def configure_application(services: Container, _: Settings) -> Application:
    app_ = Application(services=services, show_error_details=True)

    docs.bind_app(app_)
    configure_error_handlers(app_)
    return app_


def get_app() -> Application:
    try:
        return configure_application(*configure_services())
    except Exception as e:
        return get_diagnostic_app(e)


app = get_app()

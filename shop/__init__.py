import config
import stripe
import sentry_sdk
from flask import Flask
from flask_mail import Mail
from .routes import bp as main_bp
from sentry_sdk.integrations.flask import FlaskIntegration

stripe.api_key = config.STRIPE_SECRET_KEY


def create_app(package_name=__name__, static_folder='static', template_folder='templates', **config_overrides):
    app = Flask(package_name,
                static_url_path='/assets',
                static_folder=static_folder,
                template_folder=template_folder)
    app.config.from_object(config)

    # Apply overrides
    app.config.update(config_overrides)

    Mail(app)
    app.register_blueprint(main_bp)

    if not app.debug:
        sentry_sdk.init(
            dsn=config.SENTRY_DSN,
            integrations=[FlaskIntegration()]
        )

    return app

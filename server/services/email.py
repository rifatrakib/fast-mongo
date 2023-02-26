from fastapi import Request
from fastapi.templating import Jinja2Templates
from fastapi_mail import ConnectionConfig, FastMail, MessageSchema, MessageType

from server.config.factory import settings
from server.database.user import create_new_user_activation
from server.models.user import User

templates = Jinja2Templates(directory="server/templates")


def get_mail_config():
    conf = ConnectionConfig(
        MAIL_USERNAME=settings.MAIL_USERNAME,
        MAIL_PASSWORD=settings.MAIL_PASSWORD,
        MAIL_FROM=settings.MAIL_FROM,
        MAIL_PORT=settings.MAIL_PORT,
        MAIL_SERVER=settings.MAIL_SERVER,
        MAIL_FROM_NAME=settings.MAIL_FROM_NAME,
        MAIL_STARTTLS=settings.MAIL_STARTTLS,
        MAIL_SSL_TLS=settings.MAIL_SSL_TLS,
        USE_CREDENTIALS=settings.USE_CREDENTIALS,
    )
    return conf


async def send_email(request: Request, user: User):
    user_activation_key = await create_new_user_activation(username=user.username, email=user.email)
    activation_key = user_activation_key.id
    url = f"{settings.ACTIVATION_URL}/{activation_key}"
    template = templates.TemplateResponse(
        "account-activation.html",
        {
            "request": request,
            "subject": f"Verification email for {settings.APP_NAME}",
            "url": url,
            "username": user.username,
        },
    )
    html = template.body.decode("utf-8")
    message = MessageSchema(
        subject=f"{settings.APP_NAME} user account activation",
        recipients=[user.email],
        body=html,
        subtype=MessageType.html,
    )
    mailing_agent = FastMail(get_mail_config())
    await mailing_agent.send_message(message)

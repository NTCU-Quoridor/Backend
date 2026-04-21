from fastapi_mail import ConnectionConfig, FastMail, MessageSchema, MessageType
from .config import settings

conf = ConnectionConfig (
    MAIL_USERNAME = settings.MAIL_USERNAME,
    MAIL_PASSWORD = settings.MAIL_PASSWORD,
    MAIL_FROM = settings.MAIL_FROM,
    MAIL_PORT = settings.MAIL_PORT,
    MAIL_SERVER = settings.MAIL_SERVER,
    MAIL_STARTTLS = settings.MAIL_STARTTLS,
    MAIL_SSL_TLS = settings.MAIL_SSL_TLS,
    USE_CREDENTIALS = True,
    VALIDATE_CERTS = True
)

async def send_reset_password_mail(email_to: str, token: str):
    # 重設連建，指向前端頁面
    url = f"{settings.FRONTEND_URL}/reset_password.html?token={token}"
    # reset_password.html 是預設重設密碼的頁面

    # html 基本樣式
    html = f"""
            <p>您好, </p>
            <p>請點擊下方連結重設密碼 (時效為15分鐘): </p>
            <p><a href='{url}' style="padding: 10px; background-color: #4CAF50; color: white; text-decoration: none;">Click here</a></p>
            <p>URL: {url}</p>
            """

    message = MessageSchema (
        subject = "WallGo password reset request",
        recipients = [email_to],
        body = html,
        subtype = MessageType.html
    )

    fm = FastMail(conf)
    await fm.send_message(message)
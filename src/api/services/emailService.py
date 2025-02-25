class EmailService:
    def __init__(self):
        pass

    def send_email(self, to: str, subject: str, body: str):
        print(f"📧 Enviando email a {to} con asunto '{subject}'")
        # Aquí iría la lógica real de envío
        return {"status": "sent", "to": to, "subject": subject}

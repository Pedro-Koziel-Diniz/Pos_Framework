from django.contrib.sessions.models import Session

class LogoutOnRestartMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response
        self.clear_all_sessions()  # Limpa todas as sessões ao reiniciar o servidor

    def __call__(self, request):
        return self.get_response(request)

    def clear_all_sessions(self):
        """Remove todas as sessões ativas ao reiniciar o servidor"""
        try:
            Session.objects.all().delete()
            print("🔄 Todas as sessões foram limpas no reinício do servidor.")
        except Exception as e:
            print(f"⚠ Erro ao limpar sessões: {e}")

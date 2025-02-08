from django.contrib.sessions.models import Session

class LogoutOnRestartMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response
        self._cleared_sessions = False  # Evita apagar sessões várias vezes

    def __call__(self, request):
        if not self._cleared_sessions:
            self.clear_all_sessions()
            self._cleared_sessions = True  # Marca como já limpo para evitar múltiplas execuções
        
        return self.get_response(request)

    def clear_all_sessions(self):
        """Remove todas as sessões ativas ao reiniciar o servidor"""
        Session.objects.all().delete()

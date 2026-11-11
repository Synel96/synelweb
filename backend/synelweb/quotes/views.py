from rest_framework import generics, status
from rest_framework.response import Response
from rest_framework.throttling import ScopedRateThrottle

from .notifications import notify_new_quote
from .serializers import QuoteRequestSerializer


class QuoteRequestCreateAPIView(generics.CreateAPIView):
    serializer_class = QuoteRequestSerializer
    throttle_classes = [ScopedRateThrottle]
    throttle_scope = "quote_requests"
    # Public form: no session auth, so no CSRF check on this endpoint.
    authentication_classes = []
    permission_classes = []

    def create(self, request, *args, **kwargs):
        # Honeypot filled in: a bot. Answer as if it worked, save nothing.
        if str(request.data.get("company", "")).strip():
            return Response({"status": "received"}, status=status.HTTP_201_CREATED)

        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        quote = serializer.save()
        notify_new_quote(quote)
        return Response({"status": "received"}, status=status.HTTP_201_CREATED)

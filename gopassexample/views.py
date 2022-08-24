import jwt
import requests
from django.conf import settings
from django.http import HttpResponseRedirect, JsonResponse
from django.shortcuts import redirect
from django.utils import timezone
from django.views.generic import FormView, TemplateView, View

from .client import GoPass
from .forms import GoPassForm


class IndexView(FormView):
    template_name = "index.html"
    form_class = GoPassForm
    success_url = "/thanks/"

    def get_remote_ip(self):
        x_forwarded_for = self.request.META.get("HTTP_X_FORWARDED_FOR")
        if x_forwarded_for:
            ip = x_forwarded_for.split(",")[0]
        else:
            ip = self.request.META.get("REMOTE_ADDR")
        return ip

    def get_initial(self):
        initial = super().get_initial()
        initial["remote_ip"] = self.get_remote_ip()
        return initial

    def form_valid(self, form):
        gopass = GoPass(settings.GOBO_CLIENT_SECRET)
        return redirect(
            gopass.generate_url(
                {k: v for k, v in form.cleaned_data.items() if v},
                settings.GOBO_DOMAIN,
                ssl=False,
            )
        )


class APIView(View):
    def dispatch(self, request, *args, **kwargs):
        auth = request.headers.get("Authorization", "").split()

        token = None
        if auth and auth[0].lower() == "bearer" and len(auth) == 2:
            token = auth[1]

        token_payload = None
        if token:
            try:
                token_payload = jwt.decode(
                    jwt=token,
                    key=settings.GOBO_CLIENT_SECRET,
                    algorithms=["HS256"],
                    options={"verify_aud": False},
                )
            except Exception as e:
                print(e)

        return JsonResponse(
            {
                "method": request.method,
                "access_token": token,
                "token_payload": token_payload,
                "timestamp": timezone.now(),
            }
        )


class InstallView(View):
    def get(self, request, *args, **kwargs):
        return HttpResponseRedirect(
            f"http://{settings.GOBO_DOMAIN}"
            f"/oauth/authorize?client_id={settings.APP_CLIENT_ID}&response_type=code"
        )


class CallbackView(TemplateView):
    template_name = "callback.html"

    def get(self, request, *args, **kwargs):
        code = request.GET.get("code")
        if not code:
            error = request.GET.get("error")
            return HttpResponseRedirect(
                f"http://{settings.GOBO_DOMAIN}/redirect?error_message={error}"
            )

        try:
            r = requests.post(
                f"http://{settings.GOBO_DOMAIN}/oauth/token",
                {
                    "client_id": settings.APP_CLIENT_ID,
                    "client_secret": settings.APP_CLIENT_SECRET,
                    "grant_type": "authorization_code",
                    "code": code,
                },
            )
            r.raise_for_status()
        except requests.exceptions.HTTPError as e:
            reason = e.response.reason
            return HttpResponseRedirect(
                f"http://{settings.GOBO_DOMAIN}/redirect?error_message={reason}"
            )

        data = r.json()
        access_token = data["access_token"]
        print(f"access token: {access_token}")

        return HttpResponseRedirect(
            f"http://{settings.GOBO_DOMAIN}/redirect?install_success=true"
        )

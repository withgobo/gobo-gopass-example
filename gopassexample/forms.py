import uuid

from django import forms


class GoPassForm(forms.Form):
    guid = forms.UUIDField(label="Gobo GUID", required=True)
    guid.widget.attrs.update(placeholder=uuid.uuid4, autofocus=True)

    next = forms.CharField(label="Next URL", required=False)
    next.widget.attrs.update(placeholder="/marketplace/")

    remote_ip = forms.GenericIPAddressField(label="Remote IP", required=False)
    remote_ip.widget.attrs.update(placeholder="127.0.0.1")

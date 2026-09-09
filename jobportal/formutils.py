from django import forms


class BootstrapFormMixin:
    """
    Mixin that gives every field in a form a Bootstrap 5 class
    automatically, so templates don't need to style each input by hand.
    Mix this in ahead of forms.Form / forms.ModelForm (or Django's
    built-in forms like AuthenticationForm), e.g.:

        class MyForm(BootstrapFormMixin, forms.ModelForm):
            ...
    """

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields.values():
            widget = field.widget
            existing = widget.attrs.get("class", "")

            if isinstance(widget, forms.CheckboxInput):
                css_class = "form-check-input"
            elif isinstance(widget, (forms.Select, forms.SelectMultiple)):
                css_class = "form-select"
            else:
                css_class = "form-control"

            widget.attrs["class"] = f"{existing} {css_class}".strip()

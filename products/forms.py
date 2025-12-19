from django import forms
from .models import Product
from accounts.models import VendorProfile


class ProductForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = ['vendor', 'category', 'name', 'description', 'price', 'stock', 'image', 'is_active']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # show vendor by shop name
        self.fields['vendor'].queryset = VendorProfile.objects.select_related('user').all()
        try:
            # Django ModelChoiceField supports label_from_instance on the field itself when subclassed,
            # but we can set choices labels via queryset mapping if necessary. Keep it simple.
            pass
        except Exception:
            pass


class VendorProductForm(forms.ModelForm):
    class Meta:
        model = Product
        # vendors should not choose a different vendor; vendor is set from request.user
        fields = ['category', 'name', 'description', 'price', 'stock', 'image', 'is_active']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # add Bootstrap classes to widgets for aligned inputs
        for name, field in self.fields.items():
            widget = field.widget
            attrs = widget.attrs or {}
            # file inputs and selects use form-control in Bootstrap 5; checkboxes use form-check-input
            input_type = getattr(widget, 'input_type', '')
            if input_type == 'checkbox':
                attrs['class'] = attrs.get('class', '') + ' form-check-input'
            else:
                attrs['class'] = attrs.get('class', '') + ' form-control'
            widget.attrs = attrs

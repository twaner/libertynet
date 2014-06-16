import autocomplete_light
from Equipment.models import Part

autocomplete_light.Register(
    Part,
    search_fields=['^category', 'name'],
    attrs={
        'placeholder': 'other model name',
        'data-autocomplete-minimum-characters': 1,
    },
    widget_attrs={
        'data-widget-maximum-values': 20,
        # Enable modern-style widget !
        'class': 'modern-style',
    },
)



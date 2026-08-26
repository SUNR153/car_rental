from modeltranslation.translator import register, TranslationOptions
from .models import Car

@register(Car)
class CarTranslation(TranslationOptions):
    fields = ('brand', 'model')
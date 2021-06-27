from django.contrib.auth.models import User
from .models import Product, Setting


def get_currency():
    currency, is_created = Setting.objects.get_or_create(key="currency")

    if is_created:
        currency.value = "GHC"
        currency.save()

    return currency.value


def get_company():
    company, is_created = Setting.objects.get_or_create(key="company")

    if is_created:
        company.value = "Office Lunch"
        company.save()

    return company.value





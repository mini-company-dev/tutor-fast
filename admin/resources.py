from fastapi_admin.resources import Model
from app.models.grammar_test import GrammarTest


class GrammarAdmin(Model):
    label = "Grammar"
    model = GrammarTest
    icon = "fas fa-book"

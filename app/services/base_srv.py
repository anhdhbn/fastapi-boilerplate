from fastapi import Depends

from app.core.dependencies import lang_header
from app.i18n.lang import MultiLanguage
from app.repositories.provider import Provider


class BaseSrv:
    def __init__(
        self,
        lang: MultiLanguage = Depends(lang_header),
        provider: Provider = Depends(),
    ):
        self.lang = lang
        self.provider = provider

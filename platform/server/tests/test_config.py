from app.core.config import settings

def test_settings_load():
    assert settings.APP_NAME == "Ascendrite"
    assert settings.JWT_ALGORITHM == "HS256"

from app.core.config import settings

def test_settings_load():
    assert settings.APP_NAME == "Ascendrite"
    assert settings.JWT_ALGORITHM == "HS256"
    
    # Assert runtime profile helpers
    assert settings.current_profile in ["development", "testing", "production", "staging"]
    if settings.current_profile == "development":
        assert settings.is_development is True
        assert settings.is_testing is False
        assert settings.is_production is False
    
    # Assert feature flags helpers
    assert settings.is_feature_enabled("ai") is True
    assert settings.is_feature_enabled("search") is True
    assert settings.is_feature_enabled("nonexistent_feature") is False


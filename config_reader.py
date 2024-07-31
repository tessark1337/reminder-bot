from pydantic_settings import BaseSettings, SettingsConfigDict
from pydantic import SecretStr


class Settings(BaseSettings):
    # Желательно вместо str использовать SecretStr
    # для конфиденциальных данных, например, токена бота
    bot_token: SecretStr

    model_config = SettingsConfigDict(env_file='.env', env_file_encoding='utf-8')

# При импорте файла сразу создастся
# и провалидируется объект конфига,
# который можно далее импортировать из разных мест
config = Settings()


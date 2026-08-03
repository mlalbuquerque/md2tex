class Md2TexError(RuntimeError):
    """Erro controlado do conversor."""


NetraMd2TexError = Md2TexError


class ConfigError(Md2TexError):
    """Arquivo de configuração ausente ou malformatado."""


class DependencyError(Md2TexError):
    """Dependência externa ausente."""


class ValidationError(Md2TexError):
    """Falha de validação."""


class CompilationError(Md2TexError):
    """Falha de compilação LaTeX."""

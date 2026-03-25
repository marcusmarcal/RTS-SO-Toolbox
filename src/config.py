import os

def get_env_variable(var_name):
    """Get the value of an environment variable"""
    try:
        return os.environ[var_name]
    except KeyError:
        raise RuntimeError(f'Environment variable {var_name} not found')

# Example usage:
# database_url = get_env_variable('DATABASE_URL')
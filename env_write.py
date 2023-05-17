def write_to_env_file(api_key):
    env_vars = {}
    with open('.env', 'r') as env_file:
        for line in env_file:
            line = line.strip()
            if line:
                key, value = line.split('=', 1)
                env_vars[key] = value
    
    env_vars['API_KEY'] = api_key
    
    with open('.env', 'w') as env_file:
        for key, value in env_vars.items():
            env_file.write(f"{key}={value}\n")
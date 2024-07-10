import os

import dotenv

def update_env_var(env_var_name, env_var_value, verbose):
    try:
        dotenv_file = dotenv.find_dotenv(raise_error_if_not_found=True)
        print("Updating .env file at " + dotenv_file + "? (y/n)")
        choice = input()
        if choice != "y":
            print("No .env file updated. Exiting.")
    except IOError:
        print("No .env file found.")
        print("Creating a new .env file at user home directory? (y/n)")
        choice = input()
        if choice == "y":
            dotenv_file = os.environ.get("HOME") + "/.env"
        else:
            print("No .env file created. Exiting.")
            return
    dotenv.set_key(dotenv_file, env_var_name, env_var_value)
    if verbose:
        print(f"Environment variable {env_var_name} has been updated to {env_var_value}.")
        print(f"env file: {dotenv_file} has been updated.")
    dotenv.load_dotenv(dotenv_file, override=True)
    return




def setup_wizard(provider_key_dict):
    # Ask which provider they want to use
    print("Welcome to the MLLM setup wizard!")
    print("This wizard will help you set up your environment to use MLLM.")
    print("Please select which provider you would like to use.")
    for i, provider in enumerate(provider_key_dict.keys()):
        print(f"{i + 1}. {provider}")
    provider_choice = input("Enter the number of the provider you would like to use: ")
    provider_choice = int(provider_choice)
    provider_choice -= 1
    provider = list(provider_key_dict.keys())[provider_choice]

    print(f"Great! You have selected {provider} as your provider.")

    print(f"You have to set the following environment variables to use {provider}:")
    not_set = False
    for env_var in provider_key_dict[provider]:
        env_var_value = os.environ.get(env_var)
        if env_var_value is None:
            not_set = True
            print(f"{env_var} (current: None)")
        else:
            print(f"{env_var} (current: {env_var_value})")
    if not_set:
        print(
            "Some of the environment variables are not set. Do you want to set them? (y/n)")
    else:
        print("All environment variables are set. Do you want to change them? (y/n)")
    choice = input()
    if choice == "y":
        for env_var in provider_key_dict[provider]:
            env_var_value = input(f"Enter the value for {env_var}: ")
            update_env_var(env_var, env_var_value, verbose=True)
            assert os.environ[env_var] == env_var_value
        print("Environment variables set!")
    else:
        print("Environment variables not set.")

    print("Setup wizard ended. The environment variables are:")
    for env_var in provider_key_dict[provider]:
        print(f"{env_var}: {os.environ.get(env_var)}")


if __name__ == '__main__':
    provider_key_dict = {"openai": ["OPENAI_API_KEY"], "anthropic": ["ANTHROPIC_API_KEY"],
                         "gemini": ["GEMINI_API_KEY"]}
    setup_wizard(provider_key_dict)

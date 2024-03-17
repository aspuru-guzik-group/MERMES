# check if the environment variable is already set
# if so exit
if [ -n "$ANTHROPIC_API_KEY" ]; then
  echo "ANTHROPIC_API_KEY is already set. Exiting."
  exit 0
fi


echo "Please enter your Anthropic API key (it looks like 'sk-...'):"
read -r API_KEY

# check terminal type
# if it is bash
# Path: script/setup_env.sh
if [ -n "$BASH_VERSION" ]; then
  echo "export ANTHROPIC_API_KEY=$API_KEY" >> ~/.bashrc
  source ~/.bashrc
fi
if [ -n "$ZSH_VERSION" ]; then
  echo "export ANTHROPIC_API_KEY=$API_KEY" >> ~/.zshrc
  source ~/.zshrc
fi
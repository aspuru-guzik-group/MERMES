echo "Please enter your OpenAI API key (it looks like 'sk-...'):"
read -r API_KEY

# check terminal type
# if it is bash
# Path: script/setup_env.sh
if [ -n "$BASH_VERSION" ]; then
  echo "export OPENAI_API_KEY=$API_KEY" >> ~/.bashrc
  source ~/.bashrc
fi
if [ -n "$ZSH_VERSION" ]; then
  echo "export OPENAI_API_KEY=$API_KEY" >> ~/.zshrc
  source ~/.zshrc
fi
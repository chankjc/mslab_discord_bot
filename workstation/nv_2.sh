if [[ -d "$HOME/.local/bin" ]] && [[ ! $PATH =~ .*"$HOME/.local/bin".* ]]; then
    PATH="$HOME/.local/bin:$PATH"
fi
python .check_server_status_2.py

curl -LsSf https://astral.sh/uv/install.sh | sh
. $HOME/.local/bin/env
echo $PATH
which uv  # Должно вывести /opt/render/.local/bin/uv
uv --version  # Должно вывести версию, например, 0.6.8
make install

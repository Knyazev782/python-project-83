chmod +x build.sh
curl -LsSf https://astral.sh/uv/install.sh | sh
source ~/.venv/bin/activate
echo $PATH
which uv  # Должно вывести /opt/render/.local/bin/uv
uv --version  # Должно вывести версию, например, 0.6.8
make install


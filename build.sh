curl -LsSf https://astral.sh/uv/install.sh | sh
export PATH="$HOME/.local/bin:$PATH"
uv --version
make install
psql -a -d "$DATABASE_URL" -f database.sql
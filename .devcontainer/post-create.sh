#!/usr/bin/env bash
# .devcontainer/post-create.sh
# Runs once when the Codespace is first built.
set -e

echo "============================================"
echo " Architex BIM AI – Codespace setup"
echo "============================================"

echo ""
echo "[1/4] Upgrading pip..."
python -m pip install --upgrade pip --quiet

echo ""
echo "[2/4] Installing Python packages (requirements.txt)..."
pip install --no-cache-dir -r requirements.txt

echo ""
echo "[3/4] Installing PyTorch (CPU-only) + PyTorch Geometric..."
# CPU-only torch keeps the codespace lean (no GPU on free tier anyway).
pip install --no-cache-dir \
    torch torchvision \
    --index-url https://download.pytorch.org/whl/cpu

pip install --no-cache-dir torch-geometric

echo ""
echo "[4/4] Installing Wrangler CLI (Cloudflare Workers)..."
npm install -g wrangler --silent

echo ""
echo "============================================"
echo " Setup complete. Useful commands:"
echo "   python scripts/generate_test_ifc.py        → generate test IFC"
echo "   python scripts/ifc_to_mesh.py --help       → mesh converter"
echo "   jupyter lab --port 8888 --no-browser       → Jupyter"
echo "   wrangler dev workers/api/index.js          → Cloudflare Worker local"
echo "============================================"

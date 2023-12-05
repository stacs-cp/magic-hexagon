
# installing python dependencies in a virtual environment
# rm -rf myenv
python3 -m venv myenv
source myenv/bin/activate
pip install -qr requirements.txt

python3 native.py

deactivate

export LD_LIBRARY_PATH=-L/Users/ozgurakgun/Downloads/or-tools_arm64_macOS-14.1_cpp_v9.8.3296/lib:$LD_LIBRARY_PATH

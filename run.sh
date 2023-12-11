
# installing python dependencies in a virtual environment
# rm -rf myenv
python3 -m venv myenv
source myenv/bin/activate
pip install -qr requirements.txt

mkdir -p outputs

python3 generate-params.py

parallel --no-notice \
    --eta \
    --joblog outputs/joblog.tsv \
    --results outputs/results \
    conjure solve abnormal.essence {} --solver=or-tools --output-format=json --solver-options "--threads 8" ::: *.param

parallel --no-notice \
    --eta \
    --joblog outputs/joblog.tsv \
    --results outputs/results \
    python3 plot.py {} ::: conjure-output/*.solution.json

deactivate

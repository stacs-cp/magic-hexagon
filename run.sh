
# installing python dependencies in a virtual environment
# rm -rf myenv # if needed
python3 -m venv myenv
source myenv/bin/activate
pip install -qr requirements.txt

mkdir -p outputs

# also generates commands.txt
python3 generate-params.py

parallel --no-notice \
    --eta \
    --joblog outputs/joblog1.tsv \
    --results outputs/results1 \
    --timeout 3600 \
    :::: commands.txt

parallel --no-notice \
    --eta \
    --joblog outputs/joblog2.tsv \
    --results outputs/results2 \
    python3 plot.py {} ::: conjure-output*/*.solution.json

rm -rf *.param

mkdir -p results
python3 collect-results.py

deactivate

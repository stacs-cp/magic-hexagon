
mkdir -p results
conjure --version > results/versions.txt
savilerow -help | head -n1 >>  results/versions.txt

# installing python dependencies in a virtual environment
# rm -rf myenv # if needed
python3 -m venv myenv
source myenv/bin/activate
pip install -qr requirements.txt

# also generates commands.txt
python3 generate-params.py

parallel --no-notice \
    --eta \
    --joblog results/joblog1.tsv \
    --results results/results1 \
    --timeout 3600 \
    :::: commands.txt

parallel --no-notice \
    --eta \
    --joblog results/joblog2.tsv \
    --results results/results2 \
    python3 plot.py {} ::: conjure-output*/*.solution.json

rm -rf *.param

python3 collect-results.py

deactivate

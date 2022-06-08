conda update -n base -c defaults conda
conda install conda-build

conda create -n coq_serapy python=3.9
conda activate coq_serapy

pip install -r requirements.txt
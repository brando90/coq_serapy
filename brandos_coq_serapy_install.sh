# - install python: https://stackoverflow.com/questions/49118277/what-is-the-best-way-to-install-conda-on-macos-apple-mac
# install brew
/bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"
#  install wget to get miniconda
brew install wget

# - install miniconda
wget https://repo.anaconda.com/miniconda/Miniconda3-latest-MacOSX-x86_64.sh -O ~/miniconda.sh
bash ~/miniconda.sh -b -p $HOME/miniconda
# source /Users/my_username/opt/anaconda3/bin/activate
source ~/miniconda/bin/activate
conda init zsh
# conda init
conda update -n base -c defaults conda
conda install conda-build

conda create -n coq_serapy python=3.9
conda activate coq_serapy
#conda remove --name metalearning2 --all

# - install opam
brew install opam
# https://stackoverflow.com/questions/72522266/how-does-one-install-opam-with-conda-for-mac-apple-os-x
# conda install -c conda-forge opam
opam init
# if doing local env? https://stackoverflow.com/questions/72522412/what-does-eval-opam-env-do-does-it-activate-a-opam-environment
#eval $(opam env)

# - install coq: see https://stackoverflow.com/questions/71117837/how-does-one-install-a-new-version-of-coq-when-it-cannot-find-the-repositories-i
# local install
#opam switch create . 4.12.1
#eval $(opam env)
#opam repo add coq-released https://coq.inria.fr/opam/released
#opam install coq

# If you want a single global (wrt conda) coq installation (for say your laptop):
opam switch create 4.12.1
opam switch 4.12.1
opam repo add coq-released https://coq.inria.fr/opam/released
opam install coq

# - install coq-serapi
opam install coq-serapi

# - install utop
opam install utop

# - coq_serapy installs
pip install -r requirements.txt
pip install -e ~/coq_serapy
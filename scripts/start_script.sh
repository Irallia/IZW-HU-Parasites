
# ---------------- Installing latest R(3.2.5) on Debian Jessie ----------------

# Appends the CRAN repository to your sources.list file 
# You could replace jessie-cran3 by the newer one
# Find the correct value at https://cloud.r-project.org/
sudo sh -c 'echo "deb http://cran.rstudio.com/bin/linux/debian jessie-cran3/" >> /etc/apt/sources.list'

# Adds the CRAN GPG key, which is used to sign the R packages for security.
sudo apt-key adv --keyserver subkeys.pgp.net --recv-key 381BA480
sudo apt-get update
sudo apt-get install r-base r-base-dev

# ---------------- Java ----------------

# install OpenJDK 8
sudo sh -c 'echo "deb http://ftp.de.debian.org/debian jessie-backports main" >> /etc/apt/sources.list'
sudo apt-get update
sudo apt-get install openjdk-8-jdk

# or

# # install Oracle JDK 8
# sudo add-apt-repository ppa:webupd8team/java
# sudo apt-get update
# sudo apt-get install oracle-java8-installer
# # or make sure that JDK 8 is default
# sudo apt-get install oracle-java8-set-default
# # or not
# sudo apt-get install --no-install-recommends oracle-java8-installer


# to retrieve curl-config
# otherwise you may have a problem with RCurl
sudo apt-get install libcurl4-gnutls-dev

# # in R
# install.packages ("h2o")

# TODO print statement install R packages in R!!! rglobi, ape, castor
# ---------------- install R packages ----------------

R CMD install rglobi

cd data

# ---------------- get tree ----------------

if wget -q http://files.opentreeoflife.org/synthesis/opentree9.1/opentree9.1_tree.tgz -nv; then echo "OTT DL succesful"; else echo "OTT DL-link broken" 1>&3; exit 1;  fi    # download OTT and post error msg if link is unreachable
tar -xf opentree9.1_tree.tgz                #untar OTT
rm opentree9.1_tree.tgz                     #remove .tar

# ---------------- get interactions ----------------

cd ../scripts/R
Rscript get_interactions.R > interactions_log.txt &


# ---------------- simulation ----------------
cd ../../simulation
sudo apt-get install python3

sudo pip install biopython
sudo pip install pandas
sudo apt-get install python3-dev
sudo pip install rpy2

R CMD install ape

python3 main.py


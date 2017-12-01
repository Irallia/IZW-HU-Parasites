
# ---------------- Installing latest R(3.2.5) on Debian Jessie ----------------

# Appends the CRAN repository to your sources.list file 
# You could replace jessie-cran3 by the newer one
# Find the correct value at https://cloud.r-project.org/
sudo sh -c 'echo "deb http://cran.rstudio.com/bin/linux/debian jessie-cran3/" >> /etc/apt/sources.list'

# Adds the CRAN GPG key, which is used to sign the R packages for security.
sudo apt-key adv --keyserver subkeys.pgp.net --recv-key 381BA480
sudo apt-get update
sudo apt-get install r-base r-base-dev

# ---------------- add missing folders ----------------

mkdir data
cd data
mkdir interaction_data

# ---------------- get interactions ----------------

cd ../scripts/R
Rscript get_interactions.R



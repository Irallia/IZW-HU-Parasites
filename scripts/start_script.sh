
# ---------------- Installing latest R(3.2.5) on Debian Jessie ----------------

# # Appends the CRAN repository to your sources.list file 
# # You could replace jessie-cran3 by the newer one
# # Find the correct value at https://cloud.r-project.org/
# sudo sh -c 'echo "deb http://cran.rstudio.com/bin/linux/debian jessie-cran3/" >> /etc/apt/sources.list'

# # Adds the CRAN GPG key, which is used to sign the R packages for security.
# sudo apt-key adv --keyserver subkeys.pgp.net --recv-key 381BA480
# sudo apt-get update
# sudo apt-get install r-base r-base-dev

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

# ---------------- install R packages ----------------

R CMD install rglobi

# ---------------- add missing folders ----------------

mkdir data
cd data
mkdir interaction_data

# ---------------- get interactions ----------------

cd ../scripts/R
Rscript get_interactions.R



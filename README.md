# onetlib_analysis
Deployed to https://bravedemo.herokuapp.com/

## Installation
Make sure docker is installed

1. Clone this repository 
    `git clone https://github.com/NickDee96/bravedemo.git`
2. Change directory to the repo's directory 
    `cd bravedemo`
3. Build the container
    `sudo docker build --tag bravedemo .` for Linux\Debian 
    `docker build --tag bravedemo .` for Windows
4. Run the container
    `sudo docker run --name viz1 -d -p 8080:8080 dataviz` for Linux\Debian
    `docker run --name viz1 -d -p 8080:8080 dataviz` for Linux\Debian 

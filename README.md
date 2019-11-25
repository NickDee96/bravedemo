# onetlib_analysis
Deployed to https://bravedemo.herokuapp.com/

## Installation
Make sure docker is installed

1. Clone this repository&nbsp;
    `git clone https://github.com/NickDee96/bravedemo.git`&nbsp;
2. Change directory to the repo's directory&nbsp;
    `cd bravedemo`
3. Build the container&nbsp;
    `sudo docker build --tag bravedemo .` for Linux\Debian &nbsp;
    `docker build --tag bravedemo .` for Windows&nbsp;
4. Run the container&nbsp;
    `sudo docker run --name viz1 -d -p 8080:8080 dataviz` for Linux\Debian&nbsp;
    `docker run --name viz1 -d -p 8080:8080 dataviz` for Linux\Debian&nbsp;
5. Access the app by opening `127.0.0.1:8080`on your browser.
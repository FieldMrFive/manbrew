Manbrew
===============
Manage manually installed (C++) libraries (for cmake) along with Homebrew in OSX.<br/>
I write this in case of
* Install some self-writen libraries, which are still in develop mode.
* Homebrew does not have the Formula and do not want to make a Formula or Tap.
* Homebrew Formula does not have the desired options and do not want to modify Formula.
* Do not want to **`sudo`**`make install` anything.
* Want Homebrew style clean _symbol link_ management.

# Install
## Dependencies
Python 3.6+

## Download
Clone the repository to wherever you like, e.g:

    git clone https://github.com/KuangyeChen/manbrew.git ~/.Manbrew

Link the `{manbrew_install_path}/manbrew` to wherever under your `PATH`, e.g:
    
    ln -s ~/.Manbrew/manbrew /usr/local/bin/manbrew

# Usage
Build the library from source with _install prefix_ set to `{manbrew_install_path}/Containers/{library_name}` e.g:

    cmake -DCMAKE_INSTALL_PREFIX=`manbrew root`/containers/opencv ..

Then `manbrew link {library_name}`, e.g:

    manbrew link opencv

All done.
## Subcommands
Subcommand | Description
---------- | -----------
link       | link container
unlink     | unlink container
remove     | remove container
list       | list all containers
root       | print manbrew root path

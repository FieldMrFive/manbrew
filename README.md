Manbrew
===============
Manage manually installed (C++) libraries (for cmake) along with Homebrew in OSX.<br/>
I write this in case of
* Homebrew does not have the Formula.
* Homebrew Formula does not have the desired options and do not want to modify Formula.
* Do not want to **`sudo`**`make install` anything.
* Want Homebrew style clean _symbol link_ management.

# Install
## Dependencies
1. Homebrew
2. brew install _cmake python@2_
3. pip install _pyyaml_

## Download
Clone the repository to wherever you like, e.g:

    git clone https://github.com/FieldMrFive/manbrew.git ~/.manbrew

Put `{manbrew_install_path}/bin` to your `PATH`, or link the `{manbrew_install_path}/bin/manbrew` to wherever under your `PATH`, e.g:
    
    echo "export PATH=$HOME/.manbrew/bin:$PATH" >> ~/.bashrc

# Usage
Build the library from source with _install prefix_ set to `{manbrew_install_path}/containers/{library_name}` e.g:

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
root       | print manbrew install path

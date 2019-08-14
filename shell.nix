# modified version of code from https://nixos.org/nixpkgs/manual/#how-to-consume-python-modules-using-pip-in-a-virtualenv-like-i-am-used-to-on-other-operating-systems

let
  # use a pinned version of nixpkgs for reproducability
  pkgs = import (builtins.fetchTarball {
    # Descriptive name to make the store path easier to identify
    name = "nixpkgs-18.09-2019-06-24";
    # rev obtained with `git ls-remote https://github.com/nixos/nixpkgs-channels nixpkgs-18.09-darwin`
    url = "https://github.com/nixos/nixpkgs/archive/3d4459e31bdccfb581e27dfffbec44d62d121349.tar.gz";
    # hash obtained with `nix-prefetch-url --unpack <url from above>`
    sha256 = "08pzpwxjrf8p7z0hcw5nhwrm6rw180g5446aandl41zvqvdjhigb";
  }) {};

  # without these I was getting `psutil/_psutil_osx.c:37:10: fatal error: 'IOKit/IOKitLib.h' file not found`
  platformBuildInputs = with pkgs;
    if stdenv.isDarwin then [darwin.IOKit darwin.apple_sdk.frameworks.Carbon]
    else [];

in
  with pkgs ;

  with python36Packages;

  stdenv.mkDerivation {
    name = "impure-happy-train-pip-env";
    buildInputs = [
      virtualenv
      pip
      pylint
      sysctl
    ] ++ platformBuildInputs;
    src = null;
    shellHook = ''
    # set SOURCE_DATE_EPOCH so that we can use python wheels
    SOURCE_DATE_EPOCH=$(date +%s)
    virtualenv --no-setuptools venv
    export PATH=$PWD/venv/bin:$PATH
    # this shouldn't be necessary but Cody needs to get his editor set up properly :\
    export PYTHONPATH=$PWD/venv/lib/python3.6/site-packages:$PATH
    pip install setuptools==41.0.1
    pip install -r requirements-frozen.txt
    '';
  }

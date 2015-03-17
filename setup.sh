#!/usr/bin/env bash

pushd() {
  command pushd "$@" > /dev/null
}

popd() {
  command popd "$@" > /dev/null
}

command_exists() {
  command -v "$1" > /dev/null 2>&1 ;
}

SCRIPT_DIR="$( cd "$(dirname "${BASH_SOURCE[0]}" )" && pwd )"

build_file=$SCRIPT_DIR/extern/elixir_complete/mix.exs

if [[ ! -f "$build_file" ]]; then
  echo "File $build_file doesn't exist. Did you forget to run:"
  printf "\n\tgit submodule update --init --recursive\n\n"
  exit 1
fi


if ! command_exists mix; then
  echo "Error: can't access mix in the current PATH"
  exit 1
fi

pushd $(dirname $build_file)
mix do deps.get, compile, escript.build
if [[ ! -f "elixir_complete" ]]; then
  echo "Failed to build elixir_complete escript"
  popd
  exit 1
fi
popd

echo "****SUCCESS****"


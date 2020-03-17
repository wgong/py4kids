# Simple gRPC - Greeting

## Install gRPC python packages
    $ python -m pip install grpcio
    $ python -m pip install grpcio-tools

## Create IDL in Proto buffer
    $ vi greeter.proto

## Run CodeGen to create _pb2.py, _pb2_grpc.py
    $ python run_codegen.py

## Start server
    $ python greeter_server.py

## Run clinet
    $ python greeter_client.py


# gRPC Examples

    $ git clone https://github.com/grpc/grpc.git
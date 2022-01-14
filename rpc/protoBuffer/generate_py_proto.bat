@echo off

REM ********* not contain file extension .proto************
set protos=./proto/*.proto

ECHO generating py files from proto
@REM for %%i in (%protos%) do (.\protoc_3.11.2.exe %%i --python_out=.\ )
for %%i in (./proto/%protos%) do (python -m grpc_tools.protoc --python_out=./generated/ --grpc_python_out=./generated/ -I. %%i )


@REM python -m grpc_tools.protoc --python_out=. --grpc_python_out. -I. hand.proto
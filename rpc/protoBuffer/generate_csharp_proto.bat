@echo off

set protos=*.proto

ECHO generating c# files from proto
for %%i in (%protos%) do (.\protoc_3.11.2.exe %%i --csharp_out=.\ --grpc_out=.\ --plugin=protoc-gen-grpc=grpc_csharp_plugin.exe)

::translate line end to windows style
@REM for %%i in (./*) do (.\unix2dos.exe ./%%i)





@REM ./protoc.exe --csharp_out=. --grpc_out=. --plugin=protoc-gen-grpc=grpc_csharp_plugin.exe -I. hand.proto
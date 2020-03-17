0) list streams
$ aws kinesis list-streams
{
    "StreamNames": [
        "wildrydes", 
        "wildrydes-summary"
    ]
}

1) create a stream='python-stream'
$ aws kinesis create-stream --stream-name python-stream --shard-count 1

2) delete the stream='python-stream'
$ aws kinesis delete-stream --stream-name python-stream

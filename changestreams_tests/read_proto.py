import base64
from google.protobuf import message
# Assuming you have the generated .py file from your .proto schema
from my_protobuf_schema import MyChangeStreamMessage  # This would be the class generated from your .proto file

# Example protobuf data (from your result)
protobuf_data = "[[,,2024-10-11T10:12:13.123456Z,00000002,__8BAYEHAaoH7rAAAYLAY4NTdWJzY3JpYmVyc0NoYW5nZVN0cmVhbQABhIEGBoc3MAEMgoCDCMNkAAAAAAAAhAT8qJr-hWcyNjhfNjg0NTI5OQAB__-F_wYkMKJ7a4uG_wYkMVrJOoWHgMBkAQH__w,]]"

# Clean and decode the protobuf base64 string (removing the extra characters around the data)
protobuf_base64 = protobuf_data.split("__")[1]
decoded_bytes = base64.b64decode(protobuf_base64)

# Parse the protobuf message
change_stream_message = MyChangeStreamMessage()
change_stream_message.ParseFromString(decoded_bytes)

# Now you can access the fields from the parsed message
print(change_stream_message)
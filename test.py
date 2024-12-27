import can

message1 = can.Message(arbitration_id= 123, data= [0x01, 0x02, 0x03])
message2 = can.Message(arbitration_id= 100, data= [0x01, 0x02, 0x03])
message3 = can.Message(arbitration_id= 123, data= [0x00, 0x01, 0x03])

list = [message1, message2, message3]

print(list)

list.sort(key=lambda msg: (msg.arbitration_id, msg.data))

print(list)
## Challange

After a very noisy after-work party, Harald Bluetooth's system administrators have left the local pub in a total mess. In the chaos of empty Red Bull cans and haphazardly crossed cables they left behind, Harriet has found a hastily written URL. On the webpage, there are cryptic instructions and an equally cryptic message that most likely has something to do with Bluetooth. If Harald and his henchmen have put so much effort into keeping the message a secret, it is surely something important. Help Harriet get to the bottom of this mysterious message.

Written-down URL: https://ebefa92f.0x4d555354.se

## Solve 

See decode.py that implements the following steps:

### View webpage

```
PATH 985_BT.PCAP;
SET ENCSRV TCP PORT 29182;
SET ENCLEN 127;
BEGIN;
f2e5ea97a7410a5fe613939700b93710
f12e5e7aefcc9739101f4a13042147e9
61af81d56663bc60f45f4991f397a2a7
597bb4aef320e8dc81e0cd69c339769c
d353c324cecae93cad5adaf3ba6a35d7
58299f5e47297a28791725de68befb7d
97422d8edb86da6d38fa597455dff318
5ab1fb9d5c8fd86b8e40e457009a56c7
0fac52ac04eb5261bebca6174d931d7d
1a32ce334fd7423a8027ca7085320214
42cb476155ecc6ca2644259df691956f
6d6ae41299cc8f242d8beb32af703af5
b5bc757622147ac64a897196ea3148c7
5357c921a9e12c23c9050ed5ecbbd31e
5038ffc7743e43e800e9c176f826c31c
115490ef1513765d3383f823441ee3cf
584babefc7c05aebb92d9f3a710e8612
c3cffd8c35dd03b7ed2cd63015da2f43
0c5bb83986e9990c087f0705321cddde
fd373839a823a14265953bac7e73e56d
7c474bf9d05cf3bd8acdde670b759388
10d560374dbf1a23158523e8549cddc6
befde664540868c77b776f334b9d0dfa
daead789db3c6c493db281ffe3e35847
dda20373697c4bd101419668859bda9f
af4712aa73f413cbbfa6e8df763ae8bd
fff30b5cfdecae3baca61bbd57870cfb
89436bb74d6b710aba5b88ec37e79ce2
d246761379629b2c284ce90c655c8466
46a8993dd4570343f79877d10c21613f
cea14f240c8f65e6ae50dbdcf06f2f17
a6e05f92bca0362ee4b90b91f7a39212
8e7b21bcec580bb105fe8532108c8e30
ba71a648c84da9a0377f9835057cc8c7
f9f85d2f3c6e03bc9764f60d63f0d161
e596de42114ab3c2efada484006be119
ec5435083b415fcb1775e173abe73c59
a551f04001ba9168603050117d5fe81c
082d12afed1002a89958
END;
```
### Connect to service on port 29182

The service in question operates by exchanging data in chunks of 127 bytes. 

Initial Request: You start by sending the first 127 bytes of a key to the service.
Receiving the Response: In response, the service sends back 127 bytes of data. This data is part of a PCAP file, which is a format used to capture network packets.

Subsequent Requests: To retrieve the next segment of the PCAP file, you need to send another request. This request should include:
The 127 bytes you just received (decoded bytes).
An additional 127 bytes from the key.

Repeat the Process: You continue this process, using the last received 127 bytes in combination with the next 127 bytes from the key for each new request. This sequence is repeated until you have retrieved the entire PCAP file.

## View the PCAP file 

File appears to include LCAP/Bluetooth communication. 

```
   1   0.000000   controller → host         HCI_EVT 4 Rcvd Inquiry Complete
    2   0.000984         host → controller   HCI_CMD 9 Sent Inquiry
    3   0.005993   controller → host         HCI_EVT 7 Rcvd Command Status (Inquiry)
    4   1.744294         host → controller   HCI_CMD 17 Sent Create Connection
    5   1.760702   controller → host         HCI_EVT 4 Rcvd Inquiry Complete
    6   1.761709   controller → host         HCI_EVT 7 Rcvd Command Status (Create Connection)
    7   3.727531         host → controller   HCI_CMD 9 Sent Inquiry
    8   3.738374   controller → host         HCI_EVT 7 Rcvd Command Status (Inquiry)
    9   5.730041   controller → host         HCI_EVT 14 Rcvd Connect Complete
   10   5.730066         host → controller   HCI_CMD 8 Sent Write Link Policy Settings
   11   5.731294 localhost () → Motorola_c8:cb:b2 () L2CAP 57 Sent Echo Request
   12   5.750038   controller → host         HCI_EVT 6 Rcvd Max Slots Change
   13   5.751036   controller → host         HCI_EVT 9 Rcvd Command Complete (Write Link Policy Settings)
   14   5.839023   controller → host         HCI_EVT 8 Rcvd Number of Completed Packets
   15   5.864776 Motorola_c8:cb:b2 () → localhost () L2CAP 57 Rcvd Echo Response
   16   6.866637 localhost () → Motorola_c8:cb:b2 () L2CAP 57 Sent Echo Request
   17   6.903844   controller → host         HCI_EVT 8 Rcvd Number of Completed Packets
   18   6.987832 Motorola_c8:cb:b2 () → localhost () L2CAP 57 Rcvd Echo Response
   19   9.157273         host → controller   HCI_CMD 7 Sent Disconnect
   20   9.162466   controller → host         HCI_EVT 7 Rcvd Command Status (Disconnect)
   21   9.178472   controller → host         HCI_EVT 7 Rcvd Disconnect Complete
```

## Get package 15 and 16 

Package 15 and 16 contain echo request and response. 

XOR both packages to get the flag 



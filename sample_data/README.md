# Sample Data

This folder contains sample `.olk15RecentAddresses` files to be used for testing purposes. These files **do not contain any personal information** and have been generated for this very specific purpose.

## sample2.olk15RecentAddresses

This file contains just 2 email addresses with their associated first names and last names:

```
Email                        | First Name    | Last Name  |
-----------------------------|---------------|------------|
john.smith@example.com       | John          | Smith      |
mailer-daemon@googlemail.com | Mail Delivery | Subsystem  |
```

This is a binary file, whose contents can be inspected with a **Hex Editor** (*I used open source [Hex Fied](https://hexfiend.com/)*) which is helpful for debugging and troubleshooting purposes, but difficult to parse when the file becomes large (with hundreds or thousands of contacts). Since this file is small (310 bytes), here are the contents of the file with its hex representation on the left, and its ascii representation on the right, for reference purposes.

```
D00D0000 01000000 02000000 04000000	9546E3BD 170C4B61 | Ð               Fã½  Ka
80EF5D7A 092EA217 416E6352 D1F15777 09000000 04003200 |  ï]z	.¢ AncRÑñWw	     2 
0C002200 0C001C00 0C003800 28000300 00006A6F 686E2E73 |   "       8 (     john.s
6D697468 40657861 6D706C65 2E636F6D 6D61696C 65722D64 | mith@example.commailer-d
61656D6F 6E40676F 6F676C65 6D61696C 2E636F6D 00000000 | aemon@googlemail.com    
16000000 32000000 4A006F00 68006E00 4D006100 69006C00 |     2   J o h n M a i l 
20004400 65006C00 69007600 65007200 79000000 00000800 |   D e l i v e r y       
00002200 00005300 6D006900 74006800 53007500 62007300 |   "   S m i t h S u b s 
79007300 74006500 6D000000 00000A00 00001C00 00000392 | y s t e m              
EAE20000 00000000 00000000 00000100 00000000 000000CB | êâ                     Ë
FD020000 00000000 00000692 EAE20000 00000000 00000200 | ý           êâ          
00000154 15030100 00000000 00000000 00000392 EAE20000 |    T                êâ  
00000000 00000200 00000000 00000000 0000B901 0000     |                   ¹   
```

## sample3.olkRecentAddresses

This file contains 3 email addresses with their associated first names and last names:

```
Email                        | First Name    | Last Name  |
-----------------------------|---------------|------------|
john.smith@example.com       | John          | Smith      |
alice.chan@example.com       | Alice         | Chan       |
mailer-daemon@googlemail.com | Mail Delivery | Subsystem  |
```


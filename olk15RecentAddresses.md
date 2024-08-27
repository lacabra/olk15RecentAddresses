

# olk15RecentAddresses Format

olk15RecentAddresses files are generated and managed by Outlook 15 using a proprietary binary format. Through trial and error and the efforts of multiple contributors, we have been able to infer several parts of  their file structure.

## File Structure

All files have a fixed-length header of 65 bytes, and four other sections of variable length, that store the following information:

- First Section: emails
- Second Section: first names
- Third Section: last names
- Fourth Section: unknown. We know that there is a fourth section, but we have not been able to find any meaningful information stored in there.

Each section has the same structure, which is divided in two subsections

- First subsection stores variable length strings without delimiters
- Second subsection stores the indices for each item in the first section, i.e. where the string starts.

```
+-----------------------------+
|         File Header         |  <- First 65 bytes
+-----------------------------+
|                             |
|        First Section        |  <- Emails
|  +-----------------------+  |
|  |    Variable-Length    |  |
|  |      Email Strings    |  |  <- Subsection 1 (variable length)
|  +-----------------------+  |
|  | Index for Each Email  |  |  <- Subsection 2 (variable length)
|  +-----------------------+  |
+-----------------------------+
|                             |
|        Second Section       |  <- First Names 
|  +-----------------------+  |
|  |    Variable-Length    |  |
|  |   First Name Strings  |  |  <- Subsection 1 (variable length)
|  +-----------------------+  |
|  | Index for Each Name   |  |  <- Subsection 2 (variable length)
|  +-----------------------+  |
+-----------------------------+
|                             |
|        Third Section        |  <- Last Names
|  +-----------------------+  |
|  |    Variable-Length    |  |
|  |    Last Name Strings  |  |  <- Subsection 1 (variable length)
|  +-----------------------+  |
|  | Index for Each Name   |  |  <- Subsection 2 (variable length)
|  +-----------------------+  |
+-----------------------------+
|                             |
|        Fourth Section       |  <- Unknown section
|  +-----------------------+  |
|  |    Variable-Length    |  |
|  |     Unknown Data      |  |  <- Subsection 1 (variable length)
|  +-----------------------+  |
|  |  Index for Each Item  |  |  <- Subsection 2 (variable length)
|  +-----------------------+  |
+-----------------------------+
```

## Header Structure

Let's take the header of [sample_data/sample2.olk15RecentAddresses](https://github.com/lacabra/olk15RecentAddresses/blob/main/sample_data/sample2.olk15RecentAddresses) as a reference to explain the structure, specifically at the first 65 bytes:

```
D00D0000 01000000 02000000 04000000 9546E3BD 170C4B61 80EF5D7A 092EA217 416E6352 D1F15777 09000000 04003200 0C002200 0C001C00 0C003800 28000300 0000
```

| Byte(s) | Value      | Explanation                                                  |
| ------- | ---------- | ------------------------------------------------------------ |
| 0 - 3   | `D00D0000` | Magic number or file identifier, most likely what identifies this file as an *olk15RecentAddresses* file. **Constant** value. |
| 4 - 7   | `01000000` | Possible version number, or other static metadata, these bytes remain **constant** through multiple files inspected. |
| 8 - 11  | `02000000` | Possible version number, or other static metadata, these bytes remain **constant** through multiple files inspected. |
| 12 - 15 | `04000000` | Possible version number, or other static metadata, these bytes remain **constant** through multiple files inspected. |
| 16 - 19 | `9546E3BD` | Possible checksums, timestamps, or other identifiers specific to this file. These bytes **vary** from file to file. |
| 20 - 23 | `170C4B61` | Possible checksums, timestamps, or other identifiers specific to this file. These bytes **vary** from file to file. |
| 24 - 27 | `80EF5D7A` | Possible checksums, timestamps, or other identifiers specific to this file. These bytes **vary** from file to file. |
| 28 - 31 | `092EA217` | Possible checksums, timestamps, or other identifiers specific to this file. These bytes **vary** from file to file. |
| 32 - 35 | `416E6352` | Possible checksums, timestamps, or other identifiers specific to this file. These bytes **vary** from file to file. |
| 36 - 39 | `D1F15777` | Possible checksums, timestamps, or other identifiers specific to this file. These bytes **vary** from file to file. |
| 40 - 43 | `09000000` | Static metadata, these bytes remain **constant** through multiple files inspected. |
| 44 - 45 | `0400`     | Number of sections in this file: **4** (16 bit integer with 2-bytes little-endian encoding). **Constant** value. |
| 46 - 47 | `3200`     | Offset for the start of 2nd subsection (indices) of First Section (emails) ** |
| 48 - 49 | `0C00`     | Offset for the start of Second Section (first names)         |
| 50 - 51 | `2200`     | Offset for the start of 2nd subsection (indices) of Second Section (first names) ** |
| 52 - 53 | `0C00`     | Offset for the start of Third Section (last names)           |
| 54 - 55 | `1C00`     | Offset for the start of 3rd subsection (indices) of Third Section (last names) ** |
| 56 - 57 | `0C00`     | Offset for the start of Fourth Section (unknown)             |
| 58 - 59 | `3800`     | Offset for the start of 2nd subsection (indices) of Fourth Section (unknown) ** |
| 60 - 61 | `2800`     | Unknown                                                      |
| 62 - 63 | `0300`     | Unknown, but constant of value **3**                         |
| 64 - 65 | `0000`     | End-of-section delimiter                                     |

***Note:* The offsets for the indices subsections include a 2-byte `0000` section delimiter both at the start and at the end, so if you want to process the indices from the offset obtained from the header, you have to add *2* bytes to obtain the actual start of the indices list.

## Calculating Offsets

All the offsets are relative to each other, with the first subsection (variable-length email strings) of the First Section (emails) starting at byte **66** (right after the header ends). Using the sample data above we can obtain all the section starts by continuously adding all the previous offsets:

| Bytes   | Value  | Integer | Byte position in file | Start of section    |
| ------- | ------ | ------- | --------------------- | ------------------- |
|         |        | `66`    | `66`                  | Emails              |
| 46 - 47 | `3200` | `50`    | `66` + `50` = `116`   | Emails Indices      |
| 48 - 49 | `0C00` | `12`    | `116` + `12` = `128`  | First Names         |
| 50 - 51 | `2200` | `34`    | `128` + `34` = `162`  | First Name Indices  |
| 52 - 53 | `0C00` | `12`    | `162` + `12` = `184`  | Last Names          |
| 54 - 55 | `1C00` | `28`    | `184` + `28` = `212`  | Last Name Indices   |
| 56 - 57 | `0C00` | `12`    | `212` + `12` = `224`  | 4th Section         |
| 58 - 59 | `3800` | `56`    | `212` + `56` = `268`  | 4th Section Indices |

Note that the length of all the indices sections remains constant (e.g. in this case 12), as it should be. There is the same number of fields in each section, as every email entry has an associated  first name and last name. The reason why the value is 12 in this case is because there are 2 entries in each section, encoded in 4 bytes, plus the way the offsets are calculated, they include a 2-byte `0000` delimiter both at the start and end of the indices subsection, hence: 2 + (2*4) + 2 = 12. The general case for *n* entries would be:

 2 + (n * 4) +2 = 4 + (n * 4) = 4 * (n + 1)

## Encoding

Email addresses stored in the first section are encoded using **UTF-8**, whereas first and last names stored in the second and third sections are encoded using [UTF-16LE](https://en.wikipedia.org/wiki/UTF-16) (even though big-endian is usually assumed, because this was developed by Microsoft, it uses Windows default little-endian encoding).

The lengths of each field are 16-bit integers encoded in two bytes using little-endian encoding.
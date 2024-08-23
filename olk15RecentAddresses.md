

# olk15RecentAddresses Format

olk15RecentAddresses files are generated and managed by Outlook 15 using a proprietary binary format. Through trial and error and the efforts of multiple contributors, we have been able to infer their file structure.

## File Structure

All files have a fixed-length header of 65 bytes, and four other sections of variable length, that store the following information:

- First Section: emails
- Second Section: first names
- Third Section: last names
- Fourth Section: unknown. We know that there is a fourth section, but we have not been able to find any meaningful information stored in there.

Each section has the same structure, which is divided in two subsections

- First subsection stores variable length strings without delimiters
- Second subsection stores the length of each item in the first section

```
+-----------------------------+
|         File Header         |  <- 65 bytes
+-----------------------------+
|                             |
|        First Section        |  <- Emails
|  +-----------------------+  |
|  |    Variable-Length    |  |
|  |      Email Strings    |  |  <- Subsection 1 (variable length)
|  +-----------------------+  |
|  | Length of Each Email  |  |  <- Subsection 2 (variable length)
|  +-----------------------+  |
+-----------------------------+
|                             |
|        Second Section       |  <- First Names 
|  +-----------------------+  |
|  |    Variable-Length    |  |
|  |   First Name Strings  |  |  <- Subsection 1 (variable length)
|  +-----------------------+  |
|  | Length of Each Name   |  |  <- Subsection 2 (variable length)
|  +-----------------------+  |
+-----------------------------+
|                             |
|        Third Section        |  <- Last Names
|  +-----------------------+  |
|  |    Variable-Length    |  |
|  |    Last Name Strings  |  |  <- Subsection 1 (variable length)
|  +-----------------------+  |
|  | Length of Each Name   |  |  <- Subsection 2 (variable length)
|  +-----------------------+  |
+-----------------------------+
|                             |
|        Fourth Section       |  <- Unknown section
|  +-----------------------+  |
|  |    Variable-Length    |  |
|  |     Unknown Data      |  |  <- Subsection 1 (variable length)
|  +-----------------------+  |
|  |  Length of Each Item  |  |  <- Subsection 2 (variable length)
|  +-----------------------+  |
+-----------------------------+
```

## Encoding

Email addresses stored in the first section are encoded using **UTF-8**, whereas first and last names stored in the second and third sections are encoded using [UTF-16LE](https://en.wikipedia.org/wiki/UTF-16) (even though big-endian is usually assumed, because this was developed by Microsoft, it uses Windows default little-endian encoding).

The lengths of each field are 16-bit integers encoded in two bytes using little-endian encoding.
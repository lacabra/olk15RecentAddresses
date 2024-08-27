# Outlook for OSX 2015 Recent Address Parser


This library allows you to import an **.olk15RecentAddresses** file and get back a CSV (comma-separated value) of

Email Address, First Name, LastName

## 🛠 Install

Use **Python 3**. This code has been developed and tested using Python 3.12.0. No installation is necessary beyond having Python 3 installed in your computer. Simply run the code from the command line as detailed in the next section.

## 💻 Command line

Run `main.py` to input a file and get back the contacts information, for example:

```bash
python main.py sample_data/sample2.olk15RecentAddresses
```

ouptuts:

```bash
john.smith@example.com, John, Smith
mailer-daemon@googlemail.com, Mail Delivery, Subsystem
```

## 🔎 olk15RecentAddresses files

These files are generated and managed by Outlook 15, and are found in the following folder in a MacOS computer:

```
/Users/`whoami`/Library/Group Containers/UBF8T346G9.Office/Outlook/Outlook 15 Profiles/Main Profile/Data/Recent Addresses/
```

The file structure for these files is thoroughly explained in the [accompanying documentation](olk15RecentAddresses.md).

## ✅ Tests

Unit tests are implemented using the built-in module `unittest` following the constraint of not using any external modules that would require installation. Unit tests are found in the usual `test/` folder and can be run with the following command:

```bash
python -m unittest discover -s tests
```

## 📝 License

The software contained in this repository is licensed under the [MIT License](LICENSE). Basically, the software is provided "as is", without warranty of any kind; and you can do whatever you want as long as you include the original copyright and license notice in any copy of the software/source.

## 🙏 Acknowledgements

Thanks to [The Slate Group](https://github.com/slategroup) who authored the [original repository](https://github.com/slategroup/olk15RecentAddresses) from which this one has been forked: it included the original Python 2.7 code, but was only able to extract emails. Thanks also to GitHub user [John E Jones IV](https://github.com/johnjones4) who submitted a [pull request](https://github.com/slategroup/olk15RecentAddresses/pull/4) to the original repository proposing code changes to upgrade to Python 3, that were not merged there for several years, but that inspired some code changes to this repository.


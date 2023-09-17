## HMI Data Merge

> More in depth technical guides and infos can be found in the config.xlsx "info" sheet.

***

This application was developed for a company working in the automation industry, and acted as a development tool.

There are two fundamental parts in the automation industry:
* PLC - Programmable Logic Controller
* HMI - Human Machine Interface

The PLC being the computing unit and the HMI being the graphical user interface for industry operators.

Data is shared and controlled back and forth between these components.

***

Big part of the development process consisted of getting giant excel files with many categorized sheets from the customer, which acted as blueprint for us engineers.

In addition to that, the customer provided an helpful older format excel file (lets call it sync file), containing a macro that could read the entire HMI data from the PLC and print it into this excel file.

Another macro then sent the data back into the PLC as update.

Job of the HMI Data Merge tool was to lay the giant excel from the customer right over the other and update/overwrite the sync file accordingly.

Lots of different types of instruments, equipment, sensors, motors and more came with even more specialized types. Called "typicals".

Taking all those differences into account, the tool safely updated huge amounts of data without removing or destroying a row or column.

While analyzing the data, collecting warnings, errors and potential problems, giving the engineer the least amount of work, but the best possible control.

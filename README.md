# botransactions
Transactions from BO import

Got 
ERROR: Command errored out with exit status 1:
   command: /usr/bin/python3 /tmp/tmp7cf3vs37 get_requires_for_build_wheel /tmp/tmp522h_ay0
       cwd: /tmp/pip-install-fn26zyfu/mysqlclient

The error in 1.log indicates that the pkg-config utility is not found on your system. This utility is required to locate the MySQL client library during the
installation of the mysqlclient Python package.

To resolve this issue, you need to install pkg-config and the MySQL development libraries on your system. Here are the steps to do that:

 1 Install pkg-config:
    • On Debian-based systems (like Ubuntu), you can install it using:

       sudo apt-get install pkg-config

 2 Install MySQL development libraries:
    • On Debian-based systems:

       sudo apt-get install libmysqlclient-dev

After installing these dependencies, try installing the mysqlclient package again using pip:
	
	pip install mysqlclient


Here are the shell commands to install the required dependencies:

	sudo apt-get install pkg-config libmysqlclient-dev



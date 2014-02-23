The repositroy includes tools for managing our hardware inventory based on the device42 appliance.

As starting point of the current documentation is used the documentation found on the device42 github 
repository and more specifically: [https://github.com/device42/API_Helpers](https://github.com/device42/API_Helpers)

This repository hosts a python script to easily input and retrieve data to/from device42 appliance via APIs.

### Script Provided
-----------------------------
   * d42_manage_data.py : Reads a CSV file, matches columns to arguments for APIs and sends data to device42 via POST or PUT.
   * The script will be updated soon in order to permit data retrieval. 

### Usage
-----------------------------

This script can be called with specific arguments in order to read a comma-delimited csv file of data for any of the API's supported by device42 and documented at: [http://docs.device42.com/api/](http://docs.device42.com/api/).

1. Determine which API call you need to use.

2. Note the URL of the api (e.g. /api/1.0/custom_fields/appcomp/) and the URL method (either PUT or POST).

3. Identity the mandatory fields you must include and the optional fields you wish to include.

4. Create comma separated CSV file with following:
    * The header row (first line) values must match the API field names found in the documentation.
    * After the header row, there should be one row of values for each data record that you need to send to the device42 appliance.
    * Each line in the CSV file must have a value for each mandatory field.

5: The script has to be called with the following mandatory arguments: API API_METHOD D42_PASSWORD D42_USERNAME D42_API_URL

    * `API` will be the d42 instance base url plus the api call url that you found in the API documentation.
    * `API_METHOD` will be put or post, depending on the documentation for the particular API.
    * `D42_USERNAME` and `D42_PASSWORD` are self explanatory.
    *  D42_API_URL` is the url to the installation of the device42 software. 

    Optional arguments
    * `CSV_FILE_NAME` will be the name of the csv file with data. Default is input.csv (As created in Step #4)
    * `DEBUG` can be changed to True or False, depending on how verbosdde you want the output to be.

6. After the script completes, it will print two sections of information:  The 'added' section will show all the rows that were added successfully.  The `notadded` section will have any rows that failed and the reason for the failure.

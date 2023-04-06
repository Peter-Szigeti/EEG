## Installation on Windows
For the installation you will need python and pip installed
1. Download the github repo
2. Extract its content somewhere
3. Navigate to the folder on the command line
4. Create a python virtual enviroment inside the folder with

    ```
    python3 -m venv myenv
    ```

5. Activate the enviroment

    ```
    myenv\Scripts\activate.bat
    ```

6. Install the contents of the requirements.txt

    ```
    pip install -r requirements.txt
    ```

## Using **filter_data.py**
After installing the dependencies you can run the script from the virtual enviroment.
```
python3 -m venv myenv
```
```
python3 -m Code/filter_data.py
```

You will have to input the full path to the **Mouse_EEG_ChronicSleepRestriction_Kim_et_al** folder at the start of the script.

The sessions should be fragmented into one hour fragments in a folder called **fixed**

``` ../data_BIDS/sub-0{subid}/ses-0{sessid}/eeg/fixed/ ```

And the input files should look like this

``` sub-0{subid}-{sessions[sessid]}_screew_fixed_{time}-{time+1} ```
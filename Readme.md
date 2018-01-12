# dnanexus_update_smartsheet v 1.1

## What does this app do?
This app updates smartsheet to mark completion of MokaPipe.

## What are typical use cases for this app?
This app is scheduled to run automatically once all the samples have been processed through MokaPipe .

## What data are required for this app to run?
The name of the runfolder is passed to the app as a parameter.

## How does this app work?
The app is a Python script and uses the HTTP requests module and API key to access the smartsheet GIx OPMS page.
It looks for the entry to say that this run is in progress and updates to say it is complete, and calculates the time taken.

## What does this app output?
This app updates Smartsheet as described above.

## What are the limitations of this app
The app can only access the GIx smartsheet page and requires a valid API Key.

## This app was made by Viapath Genome Informatics 




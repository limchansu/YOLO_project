`# YOLO_project

# CCTV and Calculator Integration with Server

This project demonstrates an integration between CCTV and Calculator modules using a server program. Each module provides time data to the server, which then compares the times and provides appropriate responses based on user actions.

## Modules

### cctv.py

Check the time and send it to the server only when a person is taken for the first time and the last time

### calculator.py

Whenever an item is photographed, it shows the output of 'Do you want to calculate?' and when you press yes, it sends the user's calculated time to the server

## Server Program (paymentRecord Directory)

Compare each of the time data received from CCTV.py and Calculator.py.
If the calculator's time data is not included in the time data interval taken on CCTV, it consists of two buttons

- **Click Mismatched:** Compares CCTV time data with Calculator time data. If they match, nothing is printed. If they don't match, it prints the CCTV time data.
  
- **Click Calculating:** Always prints the Calculator time data.

### Usage

To run the server program:

1. Ensure `cctv.py` and `calculator.py` are running and providing time data.
2. Start the server by running `server.py`.
3. Connect clients or simulate actions to test the server's response to "clickMismatched" and "clickCalculating" actions.

### Dependencies

- Python 3.8.19
- YOLO model (used in `cctv.py` and `calculator.py` for time data extraction)

## Example Usage

Assuming all modules are running and the server is active:


## Example with YouTube
https://youtu.be/sDBYb5-EwUA?feature=shared

# Echo Chamber
Personal project that transfers supported files from a computer to a phone.
___

# Requirements
1. **Python 3.6** or above.
    * Program makes use of formatted string literals which is only present in Python 3.6 onwards.
2. **pip**
    * Helpful to install various dependencies. Should be included when installing Python.
3. **smtplib**
    * Used to create an email whose recipient is the user's cellphone.
    * To install:
        ```console
        pip install smtplib
        ```
4. **kivy**
    * The echo chamber program uses the kivy framework to implement the GUI.
    * To install:
        ```console
        pip install kivy
        ```
5. **ffmpeg**
    * Used to compress files in order for them to be sent successfully through the phone carrier's SMS gateway.
    * To install:
        ```console
        pip install ffmpeg-python
        ```
6. **moviepy**
    * Used to convert _gif_ files into _webm_ files in order to reduce the size of the original _gif_ file.
    * To install:
        ```console
        pip install moviepy
        ```
7. **A Yahoo mail account**
    * The program currently uses yahoo mail as a middle-man to send the user text messages so a yahoo mail account is required.
___

# How to Use
1. Open the main.py module and click on "Add New Preset" to enter the required user information.
    * **NOTE**: In order to correctly login to yahoo mail through this program, the user needs to setup an **[app password](https://support.reolink.com/hc/en-us/articles/360039239274-How-to-Generate-an-APP-Password-in-Yahoo-Email-Account)** in their yahoo account and use this app password as their email password when entering their information.
![Adding New Preset GIF](/readme assets/Adding New Preset.gif)

2. Click the **"Save"** button to exit out of the preset info screen back to the main screen and click the **"Load"** button next to the desired preset.
    ![Loading Preset GIF](/readme assets/Loading Preset.gif)
3. On the left hand side of the screen, navigate to the desired file (must be a file that is supported), then click on **"Send File to Target"** to send file to cellphone as a text message attachment.


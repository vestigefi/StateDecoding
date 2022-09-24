# Repository for snippets of code used for state decoding of various Algorand applications

### How to add an application type

For a new application type, create a new file in **/src** (NOT IN src/common) named using the ID of your application type (e.g. *AF1L.py*).

You can copy a template from **/src/common/0TMP.py**. Afterward simply implement all the required methods to fit your new application type.

After you are done, add your new decoding file to **APPLICATION_TYPES** in **main.py**.

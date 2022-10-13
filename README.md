# Repository for snippets of code used for state decoding of various Algorand applications

### How to add an application type

For a new application type, create a new directory in **/src/application_types** (NOT IN src/common).
Name it using the unique ID of your application type (e.g. _TMPL_ for Template).
Keep the ID unique but as short as possible (4 characters).

You can copy a template from `/src/common/TMPL/Template.py` or `/src/common/TMPL/Template.ts`.
Afterward simply implement all the required methods to fit your new application type.

After you are done, add your new decoding file to **APPLICATION_TYPES** in **main.py** for the Python implementation and **main.ts** for the TypeScript implementation.

### Code linting

#### Python:

```
    black .
```

#### TypeScript:

```
    yarn prettier --write .
```

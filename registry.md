# Registry Tools

## Registry Shortcuts

This shortcut system lets defined identifiers replace common path sections within an
otherwise valid registry key path. As all characters are considered valid in registry
identifiers except for the backlash character (```\```), which in most languages must be
escaped (i.e., ```'\\'``` is the string containing *one* backslash). The shortcuts are
identified by two (2) consecutive backslash chracters, typically ```'\\\\'```.

Shortcuts are always identified by placing two sequential backslashes ***following*** the
shortcut identifier. If placed at the beginning, the shortcut will contain the hive name.

### Examples

Assume these shortcuts are defined. The expansions that follow would apply.

```
"_$_MS_PATH_":  "SOFTWARE\\Microsoft"
"_$CURRENT_WIN_":   "Windows\\CurrentVersion"
"_$APPX-APPS_": "Appx\\AppxAllUserStore\\Applications"
```
Shortcut-Based Paths and Expansions:
```
"_$MS_PATH_\\\\Windows\\CurentVersion\\" -->
    "SOFTWARE\\Microsoft\\Windows\\CurentVersion\\"

"SOFTWARE\\Microsoft\\_$CURRENT_WIN_\\\\Appx" -->
    "SOFTWARE\\Microsoft\\Windows\\CurrentVersion\\Appx"

"SOFTWARE\\Microsoft\\Windows\\CurrentVersion\\_$APPX-APPS_\\\\" -->
    SOFTWARE\\Microsoft\\Windows\\CurrentVersion\\Appx\\AppxAllUserStore\\Applications"
```

# Other General Rules

1) While not required, it is recommended that shortcuts begin with ```'_$'``` and end in
   ```'_'```(i.e., ```"_$shortcut_"```) for readability (so they are easy to spot in a path).
2) Shortcuts can be used together; however, they cannot overlap (i.e., a shortcut cannot
   countain a partial / complete shortcut to be expanded). They are expanded left to right:

```
"$_MS_PATH\\\\_$CURRENT_WIN_\\\\_$APPX-APPS_\\\\" -->
    SOFTWARE\\Microsoft\\Windows\\CurrentVersion\\Appx\\AppxAllUserStore\\Applications"
```

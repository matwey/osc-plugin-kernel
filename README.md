OSC Kernel Plugin
=================

This is the kernel plugin for osc (open build service console client).
The main purpose of this application is to make it easy to see that the kernel is failed again for ARM architecture ;-)

Installation
------------
Put the py-file into `~/.osc-plugins` or `/var/lib/osc-plugins`

Usage
-----
`osc ks`


Example output
--------------

```
Kernel summary:
        Kernel:HEAD     Kernel:stable   Kernel:openSUSE-13.2
i586    3.18.rc3-2      3.17.2-1        3.16.7-2            
x86_64  3.18.rc3-2      3.17.2-1        3.16.7-2            
armv6l  building        3.17.2-1                            
armv7l  3.18.rc3-2      3.17.2-1        3.16.7-2            
aarch64 building        3.17.2-1        3.16.7-2            
ppc     3.18.rc3-2      3.17.2-1        3.16.7-2            
ppc64   building        3.17.2-1        3.16.7-2            

Failed packages:
https://api.opensuse.org/build/Kernel:openSUSE-13.2/ports/ppc64le/kernel-default/_log
https://api.opensuse.org/build/Kernel:HEAD/PPC/ppc64le/kernel-default/_log
https://api.opensuse.org/build/Kernel:stable/PPC/ppc64le/kernel-default/_log
```


from distutils.core import setup, Extension

module_device = Extension('device',
                        sources = ['device.cpp'], 
                        extra_link_args =["-lstrmiids", "-lole32", "-loleaut32"]
                      )

setup (name = 'WindowsDevices',
        version = '1.0',
        description = 'Get device list with DirectShow',
        ext_modules = [module_device])

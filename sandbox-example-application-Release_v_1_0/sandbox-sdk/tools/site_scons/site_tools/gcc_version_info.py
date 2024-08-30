##############################################################################################################################
## (C) Copyright 2019 ABB. All rights reserved.
##############################################################################################################################
## Subsystem: SCons
## Description: A SCons tool that prints gcc version information to build output
##
##        NOTE: No need to call the tool. Printing happens when the tool is given to SCons env.
##
## Related documents:
##
##############################################################################################################################
def generate(env):
    """ Print gcc version information """
    env.Execute("@echo off & echo Using compiler version: &" + env['CXX'] + " --version")

def exists(env):
    return True

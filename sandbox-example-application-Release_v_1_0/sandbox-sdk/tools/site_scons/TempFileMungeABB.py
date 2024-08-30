import os
import tempfile

import SCons.Script as SC
import SCons.Errors
import SCons.Tool

class TempFileMungeABB(object):
    """A callable class.  You can set an Environment variable to this,
    then call it with a string argument, then it will perform temporary
    file substitution on it.  This is used to circumvent the long command
    line limitation.

    Example usage:
    env["TEMPFILE"] = TempFileMunge
    env["LINKCOM"] = "${TEMPFILE('$LINK $TARGET $SOURCES')}"

    By default, the name of the temporary file used begins with a
    prefix of '@'.  This may be configred for other tool chains by
    setting '$TEMPFILEPREFIX'.

    env["TEMPFILEPREFIX"] = '-@'        # diab compiler
    env["TEMPFILEPREFIX"] = '-via'      # arm tool chain
    """
    def __init__(self, cmd, prefix='@', suffix='.lnk', quote_spaces=SCons.Subst.quote_spaces):
        self.cmd = cmd
        self.prefix = prefix
        self.suffix = suffix
        self.quote_spaces = quote_spaces

    def __call__(self, target, source, env, for_signature):

        if for_signature:
            # If we're being called for signature calculation, it's
            # because we're being called by the string expansion in
            # Subst.py, which has the logic to strip any $( $) that
            # may be in the command line we squirreled away.  So we
            # just return the raw command line and let the upper
            # string substitution layers do their thing.
            return self.cmd

        # Now we're actually being called because someone is actually
        # going to try to execute the command, so we have to do our
        # own expansion.
        cmd = env.subst_list(self.cmd, SCons.Subst.SUBST_CMD, target, source)[0]
        try:
            maxline = int(env.subst('$MAXLINELENGTH'))
        except ValueError:
            maxline = 2047

        length = 0
        for c in cmd:
            # +1 is for spaces between all items, which are not noticed otherwise
            length += len(c) + 1

        if length <= maxline:
            return self.cmd

        # We do a normpath because mktemp() has what appears to be
        # a bug in Windows that will use a forward slash as a path
        # delimiter.  Windows's link mistakes that for a command line
        # switch and barfs.
        #
        # We use the .lnk suffix for the benefit of the Phar Lap
        # linkloc linker, which likes to append an .lnk suffix if
        # none is given.
        #
        # When possible, tmp file is redirected to target specific
        # build dir instead of target[0] dir which is usually lib dir
        if 'TARGET_NAME' in env:
            tempfile_dir = str(os.path.join(SC.Dir('#build').abspath, env['TARGET_NAME']))
        else:
            tempfile_dir = str(target[0].dir.abspath)

        if not os.path.exists(tempfile_dir):
            os.makedirs(tempfile_dir)
        (fd, tmp) = tempfile.mkstemp(str(self.suffix), text=True, dir=tempfile_dir)

        native_tmp = SCons.Util.get_native_path(os.path.normpath(tmp))

        if env['SHELL'] and env['SHELL'] == 'sh':
            # The sh shell will try to escape the backslashes in the
            # path, so unescape them.
            native_tmp = native_tmp.replace('\\', r'\\\\')
            # In Cygwin, we want to use rm to delete the temporary
            # file, because del does not exist in the sh shell.
            rm = env.Detect('rm') or 'del'
        else:
            # Don't use 'rm' if the shell is not sh, because rm won't
            # work with the Windows shells (cmd.exe or command.com) or
            # Windows path names.
            rm = 'del'

        #make sure that the path for the temporary file is enclosed
        #with quotes so that windows will recognize the path correctly
        #for example C:\temp would not work because of the \t
        native_tmp = str('"' + native_tmp + '"')

        cmds = list(map(self.quote_spaces, cmd))
        cmds = ' '.join(cmds)

        #find the location of the last '.exe' in the cmd string
        exe_suffixes = \
        [
            '.exe ',
            '.exe" ',
            '.exe\' '
        ]
        for exe_suffix in exe_suffixes:
            find_index = cmds.rfind(exe_suffix)
            if find_index != -1:
                break

        exec_command_index = find_index + len(exe_suffix)

        #split the cmd to two parts, first one containing the executables
        #and the second containing all the arguments and objects
        #for example exec_command contains the archiver.exe
        #and the args contains archiver flags and objects for the archiver
        exec_command = cmds[:exec_command_index].strip()
        args = cmds[exec_command_index:].strip()

        # escape backslashes ['\'] because kwwrap or other wrapper tools could strip them away otherwise
        args = args.replace('\\', '\\\\')

        if self.suffix == '.lnt':
            #this is a lint temp file call
            #lint doesnt like when argument file has quotes, so remove them
            native_tmp = native_tmp.replace('"', '')

            #remove quotes from the executable command
            #like so "lint-nt.exe" -> lint-nt.exe
            exec_command = exec_command.replace('"', '')
            #remove the lonely quote from the start of argument
            #file, otherwise lint-nt fails
            if args.startswith('" '):
                args = args[1:]

        #write the arguments to the temporary file
        string_to_write = args + "\n"
        os.write(fd, string_to_write.encode('utf-8'))

        os.close(fd)

        # XXX Using the SCons.Action.print_actions value directly
        # like this is bogus, but expedient.  This class should
        # really be rewritten as an Action that defines the
        # __call__() and strfunction() methods and lets the
        # normal action-execution logic handle whether or not to
        # print/execute the action.  The problem, though, is all
        # of that is decided before we execute this method as
        # part of expanding the $TEMPFILE construction variable.
        # Consequently, refactoring this will have to wait until
        # we get more flexible with allowing Actions to exist
        # independently and get strung together arbitrarily like
        # Ant tasks.  In the meantime, it's going to be more
        # user-friendly to not let obsession with architectural
        # purity get in the way of just being helpful, so we'll
        # reach into SCons.Action directly.
        if env.GetOption('verbose_option'):
            print("Using tempfile "+native_tmp+" for command line:\n"+
                  exec_command + " " + args)

        #return must be a single string. If list is returned, then the values are "glued" together
        #causing double-quotes to be malformed and the build will fail, for example
        #""wrapper.exe" -o "tracefile" archiver.exe ....
        return exec_command + " " + str(self.prefix) + native_tmp + '\n' + rm + " " + native_tmp

import nuke
import nukescripts
import sys
import platform
import os
import getpass
import shutil
from datetime import datetime

print ('')

def addWrite(cmdLine):
    print ('')
    print ('*****************')
    print ('starting create/ update bat file')
    print ('*****************')
    print ('')

    current_user = getpass.getuser()
    if platform.system() == "Windows":
        queueFolder = ('C:/Users/%s/.nuke/renderQueue/' % current_user)
    else:
        nuke.message("Unsupported OS")

    try:
        os.mkdir(queueFolder)
        print ('Create subfolder: ' + queueFolder)
        print ('')
    except:
        print ('Folder already exist: ' + queueFolder)
        print ('')

    batName = 'NukeRenderQueue.bat'

    batFile = os.path.join(queueFolder, batName)

    if os.path.exists(batFile):
        print ('Queue already exists! Append new commands to it...')
        print ('')

        # open file and create a list with existing commands
        writeFile = open(batFile, 'r+')

        cmdList = writeFile.readlines()

        writeFile.close()

        for h in cmdList:
            print ('')
            print h
        
        print ('')

        # append new commands to the existing list
        print ('updating queue...')
        
        cmdList.append(cmdLine)


        f = open(batFile, 'w+')

        max = len(cmdList)
        x = 1

        print ('')
        print ('***************')
        print ('writing file...')

        for line in cmdList:
            f.write('%s' % (line))
            if x < max:
                f.write('\n')
            x = x + 1

            print ('')
            print line

        f.close()

        print ('')
        print ('bat file created/ updated successfully...')
        print ('')

    else:

        print ("File doesn't exist! Creating a new one...")

        f = open(batFile, 'w+')

        #max = len(cmdQueue)
        #x = 1

        print ('')
        print ('***************')
        print ('writing file...')

        #for line in cmdQueue:
        f.write('%s' % (cmdLine))
        #if x < max:
        f.write('\n')
            #print (x)
        #x = x + 1

        print ('')
        print cmdLine

        f.close()

def WriteCMD(newWrite):
    print ('')
    print ('*****************')
    print ('starting create command lines')
    print ('*****************')
    print ('')

    nuke.scriptSave()

    nuke.root()['proxy'].setValue(False)
    CPU = 8
    env = '"%s"' % (nuke.env["ExecutablePath"])
    scriptName = '"%s"' % (nuke.scriptName())

    rFirst = str(nuke.root().firstFrame())
    rEnd = str(nuke.root().lastFrame())

    nFrameRange = rFirst + '-' + rEnd

    nVerb = '1'

    cmdQueue = []

    newWrite = newWrite.replace ('z_', '')
    newWrite = newWrite.replace ('_z', '')


    cmdLine = ('%s --nukex -i -m %s -X %s -F %s -V %s %s' % (env, CPU, newWrite, nFrameRange, nVerb, scriptName))

    print ('command lines for each Write successfully created...')
    print ('')

    addWrite(cmdLine)

def runQueue():
    print ('')
    print ('*********************')
    print ('starting render queue')
    print ('*********************')
    print ('')


    current_user = getpass.getuser()

    if platform.system() == "Windows":
        
        queueFolder = ('C:/Users/%s/.nuke/renderQueue/' % current_user)

        if os.path.exists(queueFolder):

            print('folder exists!')

            batName = 'NukeRenderQueue.bat'

            batFile = os.path.join(queueFolder, batName)

            if os.path.exists(batFile):

                print('bat file exists!')

                now = datetime.now()
                now = now.strftime("%b_%d-%H_%M_%S")

                runFile = batFile.replace('.bat', '_Doneat_%s.bat' %(now))

                print ('')
                print ('starting Terminal...')
                print ('')

                shutil.copy(batFile, runFile)

                startCMD = "start cmd /k " + runFile

                os.popen(startCMD)

                os.remove(batFile)

            else:
                nuke.message("There isn't a render list...")

        else:
            nuke.message("There isn't a render queue to run...")

def clearQueue():
    print ('')
    print ('*********************')
    print ('starting clear queue')
    print ('*********************')
    print ('')


    current_user = getpass.getuser()

    if platform.system() == "Windows":
        
        queueFolder = ('C:/Users/%s/.nuke/renderQueue/' % current_user)

        if os.path.exists(queueFolder):

            print('folder exists!')

            batName = 'NukeRenderQueue.bat'

            batFile = os.path.join(queueFolder, batName)

            if os.path.exists(batFile):

                print('erasing existing file!')

                os.remove(batFile)

            else:
                nuke.message("There isn't render list yet...")

        else:
            nuke.message("There isn't a render queue to be cleaned...")

def queueBox():
    print ('')
    print ('*****************')
    print ('starting queueBox')
    print ('*****************')
    print ('')

    rFirst = nuke.root().firstFrame()
    rEnd = nuke.root().lastFrame()

    writeNodes = nuke.allNodes('Write')

    writeNodes.sort()

    writeOn = []

    # window title
    p = nukescripts.PythonPanel('Nuke render queue')

    if len(writeNodes) > 0:

        # window label
        f = nuke.Text_Knob('title', '', '<b><font size = 6 color = green>Available Writes</b>')
        p.addKnob(f)
        f = nuke.Text_Knob('space', '', '')
        p.addKnob(f)

        # create a label and a button to each write available
        for n in writeNodes:

            if len(n.dependencies()) > 0:
                w = n.name()

                # write label
                i = nuke.Text_Knob(w, '', n.name())
                i.setFlag(nuke.STARTLINE)
                p.addKnob(i)
                writeOn.append(w)

                # create a empty space between label and button
                f = nuke.Text_Knob('space', '', '            ')
                f.clearFlag(nuke.STARTLINE)
                p.addKnob(f)

                writeName = 'z_' + str(n.name()) + '_z'

                code = 'newWrite = "%s"\nWriteCMD(newWrite)' % (writeName)

                # add button
                i = nuke.PyScript_Knob('addButton', 'add', code)
                i.clearFlag(nuke.STARTLINE)
                p.addKnob(i)

    if len(writeNodes) == 0:

        # window label
        f = nuke.Text_Knob('title', '', '<b><font size = 6 color = red>No Writes Available</b>')
        p.addKnob(f)

    f = nuke.Text_Knob('space', '', '')
    p.addKnob(f)

    # create a button to start the queue
    i = nuke.PyScript_Knob('runButton', '<b><font size = 6>run queue', 'runQueue()')
    i.setFlag(nuke.STARTLINE)
    p.addKnob(i)

    # create a button to start the queue
    i = nuke.PyScript_Knob('clearButton', '<b><font size = 6>clear queue', 'clearQueue()')
    i.clearFlag(nuke.STARTLINE)
    p.addKnob(i)

    p.setMinimumSize(350, 250)

    result = p.showModal()

    writeQueue = []

    #elif len(writeNodes) == 0:
        #nuke.message ('No write nodes in this script.\nCreate a new one a try again...')
        #return


# Add a Toolbar menu and assign a shortcut
toolbar = nuke.menu('Nodes')
cqnTools = toolbar.addMenu('CQNTools', 'Modify.png')

cqnTools.addCommand('Render Queue', 'NukeQueue.queueBox()', icon='Write.png')

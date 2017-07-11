# Copyright 2017 Kevin Froman - MIT License - https://ChaosWebs.net/

import os, imp, sys
pluginFolder = 'plugins/'
MainModule = "__init__"

def loadPlugin(plugin):
    # Loads a plugin
    return imp.load_module(MainModule, *plugin["info"])

def getPlugins(config):
    # Loads gets a plugin from the plugin folder
    # based on: https://lkubuntu.wordpress.com/2012/10/02/writing-a-python-plugin-api/
    plugins = []
    possiblePlugins = config['SITE']['plugins'].replace(' ', '').split(',')
    for i in possiblePlugins:
        location = os.path.join(pluginFolder, i)
        if not os.path.isdir(location) or not MainModule + ".py" in os.listdir(location):
            continue
        info = imp.find_module(MainModule, [location])
        plugins.append({"name": i, "info": info})
    return plugins

def events(event, data, config):
    try:
        command = sys.argv[1]
    except IndexError:
        return
    retData = ''
    #ranPlugins = [''] Doesn't seem like we need to actually do this
    for i in getPlugins(config):
        plugin = loadPlugin(i)
        #if plugin not in ranPlugins:
        try:
            if event == 'startup':
                retData = retData + plugin.startup(data)
            elif event == 'genPage':
                retData = retData + plugin.genPage(data)
            elif event == 'deletePage':
                retData = retData + plugin.deletePage(data)
            elif event == 'rebuild':
                retData = retData + plugin.rebuild(data)
            elif event == 'blogEdit':
                retData = retData + plugin.blogEdit(data)
            elif event == 'blogRebuild':
                retData = retData + plugin.blogRebuild(data)
            elif event == 'draftEdit':
                retData = retData + plugin.draftEdit(data)
            elif event == 'draftList':
                retData = retData + plugin.draftList(data)
            elif event == 'draftEdit':
                retData = retData + plugin.draftEdit(data)
            elif event == 'draftDelete':
                retData = retData + plugin.draftDelte(data)
            elif event == 'draftPublish':
                retData = retData + plugin.draftPublish(data)
            elif event == 'commands':
                if command == i['name']:
                    plugin.Commands.commands(*sys.argv)
                    retData = True
                else:
                    break
            else:
                print('Attempted to call unknown event: ' + event)
        except TypeError:
            pass
            #ranPlugins.append(plugin)
        except NameError:
            pass
    if retData == '':
        retData = data
    return retData

import platform
import logger
import sys
import PySimpleGUI as sg
import wget as net
import os
import shutil

root = os.getcwd()
argsv = sys.argv[1:]
def main():
    logger.inf('Loading...')

    logger.dbg('Checking if plugins folder exists...')
    if not os.path.isdir(f'{root}/plugins'):
        logger.wrn('Plugins folder did not exist! Creating...')
        os.mkdir(f'{root}/plugins')
        logger.dbg('Plugins folder created')
    else:
        logger.dbg('Plugins folder exists, all is good')
    plugins_root = f'{root}/plugins'
    if not os.path.isdir(f'{root}/packs'):
        logger.wrn('Packs folder did not exist! Creating...')
        os.mkdir(f'{root}/packs')
        logger.dbg('Packs folder created')
    else:
        logger.dbg('Packs folder exists, all is good')
    packs_root = f'{root}\packs'
    

    logger.dbg('Constructing mod list')
    
    no_gravity = ["https://github.com/ExoPlant/NoGravity/releases/latest/download/NoGravity.dll", "NoGravity.dll", "A"]
    too_many_explosions = ["https://github.com/AerGameChannel/TooManyExplosions/releases/latest/download/TooManyExplosions.dll", "TooManyExplosions.dll", "B"]
    harderheck = ["https://github.com/AerGameChannel/HarderHeck/releases/latest/download/HarderHeck.Mod.dll", "HarderHeck.Mod.dll", "C"]
    
    
    logger.dbg(no_gravity[1] + ' registered with ID ' + no_gravity[2])
    logger.dbg(too_many_explosions[1] + ' registered with ID ' + too_many_explosions[2])
    logger.dbg(harderheck[1] + ' registered with ID ' + harderheck[2])


    # Download NoGravity
    if not os.path.isfile(f'{plugins_root}/{no_gravity[1]}'):
        logger.inf(f'Downloading {no_gravity[1]}...')
        net.download(no_gravity[0], out=f'{plugins_root}')
        logger.inf(f'{no_gravity[1]} downloaded')
    else:
        logger.dbg(f'{no_gravity[1]} already downloaded, no need to download')

    # Download TooManyExplosions
    if not os.path.isfile(f'{plugins_root}/{too_many_explosions[1]}'):
        logger.inf(f'Downloading {too_many_explosions[1]}...')
        net.download(too_many_explosions[0], out=f'{plugins_root}')
        logger.inf(f'{too_many_explosions[1]} downloaded')
    else:
        logger.dbg(f'{too_many_explosions[1]} already downloaded, no need to download')

    # Download HarderHeck
    if not os.path.isfile(f'{plugins_root}/{harderheck[1]}'):
        logger.inf(f'Downloading {harderheck[1]}...')
        net.download(harderheck[0], out=f'{plugins_root}')
        logger.inf(f'{harderheck[1]} downloaded')
    else:
        logger.dbg(f'{harderheck[1]} already downloaded, no need to download')

    main_menu_layout = [
                       [sg.Button('Create modpack')],
                       [sg.Button('Open modpack')],
                       [sg.Button('Download BepInEx')],
                       [sg.Button('Restore Game')],
                       [sg.Button('Exit')] 
                       ]
    sg.theme('DarkGrey9')
    main_menu_window = sg.Window('Main Menu - PackWeaver', main_menu_layout)


    while True:
        main_menu_event, main_menu_values = main_menu_window.read()
        if main_menu_event == sg.WIN_CLOSED or main_menu_event == 'Exit': # if user closes window or clicks cancel
            break
        if main_menu_event == 'Restore Game':
            if platform.system() == 'Windows':
                 default_path = 'C:\Program Files (x86)\Steam\steamapps\common\Spiderheck Demo\BepInEx\plugins'
            restore_game_layout = [
                                 [sg.Text('Enter the path to your game (if not sure use the default):')],
                                 [sg.InputText(default_path)],
                                 [sg.Button('Restore'), sg.Button('Cancel')]
                                 ]
            restore_game_window = sg.Window('Enter game path', restore_game_layout)
            while True:
                    restore_game_event, restore_game_values = restore_game_window.read()
                    if restore_game_event == 'Restore':
                        game_path = restore_game_values[0]
                        if os.path.isfile(f'{game_path}/NoGravity.dll'):
                            os.remove(f'{game_path}/NoGravity.dll')
                        if os.path.isfile(f'{game_path}\TooManyExplosions.dll'):
                            os.remove(f'{game_path}\TooManyExplosions.dll')
                        if os.path.isfile(f'{game_path}\HarderHeck.Mod.dll'):
                            os.remove(f'{game_path}\HarderHeck.Mod.dll')
                        #os.remove(f'{game_path}\*')
                        sg.popup('Restored!')
                        restore_game_window.close()
                        break
                    if restore_game_event == sg.WIN_CLOSED or restore_game_event == 'Cancel': # if user closes window or clicks cancel
                        restore_game_window.close()
                        break


        if main_menu_event == 'Download BepInEx':
            if not os.path.isdir(f'{root}/cache'):
                os.mkdir(f'{root}/cache')
            net.download('https://github.com/BepInEx/BepInEx/releases/download/v5.4.19/BepInEx_x64_5.4.19.0.zip', out=f'{root}/cache')
            sg.popup('Please extract the BepInEx zip in the cache folder to your game directory (the one with the SPIDERHECK.exe)')

        if main_menu_event == 'Open modpack':
            pack_list = ''
            for pack in os.listdir(f'{root}/packs'):
                pack_list = pack_list + pack + '\n'
            pack_list_layout = [
                               [sg.Text("Packs:")],
                               [sg.Text(pack_list)],
                               [sg.Text("Pack Name:"), sg.InputText('PACK NAME')],
                               [sg.Button("Open")],
                               [sg.Button("Close")]
                               ]
            pack_list_window = sg.Window('Listing modpacks...', pack_list_layout)
            while True:
                pack_list_event, pack_list_values = pack_list_window.read()
                if pack_list_event == 'Close' or pack_list_event == sg.WIN_CLOSED:
                    pack_list_window.close()
                    break
                if pack_list_event == 'Open':
                    pack_name = pack_list_values[0]
                    pack_edit_layout = [
                                       [sg.Checkbox('NoGravity')],
                                       [sg.Checkbox('TooManyExplosions')],
                                       [sg.Checkbox('HarderHeck')],
                                       [sg.Button('Submit'), sg.Button('Launch'), sg.Button('Cancel')]
                                       ]
                    pack_root = f'{packs_root}\{pack_name}'
                    os.chdir(pack_root)
                    
                    pack_edit_window = sg.Window(f'Editing {pack_name}', pack_edit_layout)
                    pack_edit_event, pack_edit_values = pack_edit_window.read()
                    if pack_edit_event == sg.WIN_CLOSED or pack_edit_event == 'Cancel': # if user closes window or clicks cancel
                        pack_edit_window.close()
                        break
                    if pack_edit_event == 'Launch':
                        default_path = ''
                        if platform.system() == 'Windows':
                            default_path = 'C:\Program Files (x86)\Steam\steamapps\common\Spiderheck Demo\\'
                        launch_game_layout = [
                                             [sg.Text('Enter the path to your game (if not sure use the default):')],
                                             [sg.InputText(default_path)],
                                             [sg.Button('Launch'), sg.Button('Cancel')]
                                             ]
                        launch_game_window = sg.Window('Enter game path', launch_game_layout)
                        while True:
                            launch_game_event, launch_game_values = launch_game_window.read()
                            if launch_game_event == sg.WIN_CLOSED or launch_game_event == 'Cancel':
                                launch_game_window.close()
                                break
                            if launch_game_event == 'Launch':
                                game_path = launch_game_values[0]
                                plugins_path = f'{game_path}BepInEx\plugins'
                                if platform.system() == 'Windows':
                                    if os.path.isfile(f'{packs_root}/{pack_name}/NoGravity.dll'):
                                        shutil.copyfile(f'{packs_root}/{pack_name}/NoGravity.dll', f'{plugins_path}/NoGravity.dll')
                                    if os.path.isfile(f'{packs_root}/{pack_name}/TooManyExplosions.dll'):
                                        shutil.copyfile(f'{packs_root}/{pack_name}/TooManyExplosions.dll', f'{plugins_path}/TooManyExplosions.dll')
                                    if os.path.isfile(f'{packs_root}/{pack_name}/HarderHeck.Mod.dll'):
                                        shutil.copyfile(f'{packs_root}/{pack_name}/HarderHeck.Mod.dll', f'{plugins_path}/HarderHeck.Mod.dll')

                                    
                                else:
                                    os.system(f'cp {pack_root}/* {plugins_path}')
                                if launch_game_event == sg.WIN_CLOSED or launch_game_event == 'Cancel': # if user closes window or clicks cancel
                                    launch_game_window.close()
                                    break
                        if pack_edit_event == 'Submit':
                            if pack_edit_values[0]:
                                if not os.path.isfile('./NoGravity.dll'):
                                    if platform.system() == 'Windows':
                                        os.system(f'powershell -c "cp {plugins_root}/NoGravity.dll" .')
                                    else:
                                        os.system(f'cp "{plugins_root}/NoGravity.dll" .')
                            if pack_edit_values[1]:
                                if not os.path.isfile('./TooManyExplosions.dll'):
                                    if platform.system() == 'Windows':
                                        os.system(f'powershell -c "cp {plugins_root}/TooManyExplosions.dll" .')
                                    else:
                                        os.system(f'cp "{plugins_root}/TooManyExplosions.dll" .')
                            if pack_edit_values[2]:
                                if not os.path.isfile('./HarderHeck.Mod.dll'):
                                    if platform.system() == 'Windows':
                                        os.system(f'powershell -c "cp {plugins_root}/HarderHeck.Mod.dll" .')
                                    else:
                                        os.system(f'cp "{plugins_root}/HarderHeck.Mod.dll" .')
                            sg.popup('Done! Your pack has been edited')

                                       
            
        if main_menu_event == 'Create modpack':
            create_modpack_layout = [
                                    [sg.Text('Name: '), sg.InputText('Spiderheck modpack')],
                                    [sg.Checkbox('NoGravity')],
                                    [sg.Checkbox('TooManyExplosions')],
                                    [sg.Checkbox('HarderHeck')],
                                    [sg.Button('Submit'), sg.Button('Cancel')]
                                    ]
            create_modpack_window = sg.Window('Create a modpack - PackWeaver', create_modpack_layout)

            while True:
                create_modpack_event, create_modpack_values = create_modpack_window.read()
                if create_modpack_event == sg.WIN_CLOSED or main_menu_event == 'Cancel': # if user closes window or clicks cancel
                    create_modpack_window.close()
                    break
                if create_modpack_event == 'Submit':
                    pack_name = create_modpack_values[0]
                    no_gravity_enabled = create_modpack_values[1]
                    too_many_explosions_enabled = create_modpack_values[2]
                    harderheck_enabled = create_modpack_values[3]
                    if os.path.isdir(f'{packs_root}/{pack_name}'):
                        logger.err(f'Pack with name {pack_name} already exists!')
                        create_modpack_window.close()
                        break
                    os.mkdir(f'{packs_root}/{pack_name}')
                    pack_root = f'{packs_root}/{pack_name}'
                    os.chdir(pack_root)
                    if no_gravity_enabled:
                        logger.dbg('Enabling NoGravity')
                        if platform.system() == 'Windows':
                            os.system(f'powershell -c "cp {plugins_root}/NoGravity.dll" .')
                        else:
                            os.system(f'cp "{plugins_root}/NoGravity.dll" .')
                    if too_many_explosions_enabled:
                        logger.dbg('Enabling TooManyExplosions')
                        if platform.system() == 'Windows':
                            os.system(f'powershell -c "cp {plugins_root}/NoGravity.dll" .')
                        else:
                            os.system(f'cp "{plugins_root}/{too_many_explosions[1]}" .')
                    if harderheck_enabled:
                        logger.dbg('Enabling HarderHeck')
                        if platform.system() == 'Windows':
                            os.system(f'powershell -c "cp {plugins_root}/NoGravity.dll" .')
                        else:
                            os.system(f'cp "{plugins_root}/{harderheck[1]}" .')
                    sg.popup('Done! Please use Open Modpack on the front page to edit this modpack')


    logger.inf('Gracefully closing PackWeaver')
    
if __name__ == '__main__':
    main()
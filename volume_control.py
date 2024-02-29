from pycaw.pycaw import AudioUtilities, ISimpleAudioVolume, IAudioMeterInformation
import keyboard

def handle_volume(process_name, action, new_volume=None):
    sessions = AudioUtilities.GetAllSessions()

    for session in sessions:
        if session.Process and session.Process.name() == process_name:
            volume = session._ctl.QueryInterface(ISimpleAudioVolume)

            if action == "get_actual_volume":
                meter = session._ctl.QueryInterface(IAudioMeterInformation)
                
                if meter.GetPeakValue() > 0:
                    return True
                else:
                    return False

            elif action == "get_mixer_volume":
                return volume.GetMasterVolume()

            elif action == "set_mixer_volume":
                volume.SetMasterVolume(new_volume, None)

def main():
    previous_state = False

    while True:
        chrome_is_playing = handle_volume("chrome.exe", "get_actual_volume")

        if chrome_is_playing != previous_state:
            previous_state = chrome_is_playing

            if chrome_is_playing:
                handle_volume("Spotify.exe", "set_mixer_volume", 0.2)
            else:
                handle_volume("Spotify.exe", "set_mixer_volume", 1)

        if keyboard.is_pressed("insert"):
            handle_volume("Spotify.exe", "set_mixer_volume", 1)
            handle_volume("chrome.exe", "set_mixer_volume", 1)
            break

if __name__ == "__main__":
    main()
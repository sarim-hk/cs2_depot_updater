import glob
import subprocess
import threading

def get_cs2_path():
    path = input("Input your CS2 path (usually your Counter-Strike Global Offensive folder): ")
    path = path.replace("/", "\\")
    path = path.replace("'", "")
    path = path.replace('"', '')
    path = '"' + path + '"'
    return path

def get_manifest_paths():
    manifest_paths = glob.glob("./*.manifest")
    manifest_paths = [manifest[2:] for manifest in manifest_paths]
    return manifest_paths

def link_depots_to_manifests(depots, manifest_paths):
    for depot_no in depots:
        for manifest_path in manifest_paths:
            if manifest_path.startswith(depot_no):
                depots[depot_no].append(manifest_path)
    return depots

def make_commands(depots, cs2_path):
    cmds = []
    cmd = "DepotDownloader.exe -app 730 -depot DEPOTNO -validate -decryptionkey DECKEY -manifestpath MANIPATH -dir CS2DIR"
    for depot_no in depots:
        new_cmd = cmd
        new_cmd = new_cmd.replace("DEPOTNO", depot_no)
        new_cmd = new_cmd.replace("DECKEY", depots[depot_no][0])
        new_cmd = new_cmd.replace("MANIPATH", depots[depot_no][1])
        new_cmd = new_cmd.replace("CS2DIR", cs2_path)
        cmds.append(new_cmd)
    return cmds

def run_command(cmd):
    subprocess.run(cmd, shell=True, capture_output=True, text=True)

def run_commands(cmds):
    threads = {}
    for i, cmd in enumerate(cmds):
        threads[i] = threading.Thread(target=run_command, args=(cmd,))
        threads[i].start()

if __name__ == "__main__":
    import pprint
    depots = {
    "2347770": ["b23a737920b6a72f932a5bcdbdf51770d7d4d394a13f95b1cf29db28c1043d88"],
    "2347771": ["b80e2b4bd2a244ba996a013850b5d2f46c897f382164181b382c5d672fcb5090"],
    "2347779": ["a3d6504606875447dc6dedcba78bebb3e0a122fb30a504ef805536f216354271"]
    }

    cs2_path = get_cs2_path()
    manifest_paths = get_manifest_paths()
    
    depots = link_depots_to_manifests(depots, manifest_paths)
    del manifest_paths

    cmds = make_commands(depots, cs2_path)

    for cmd in cmds:
        print(cmd)

    ok_continue = input("Type OK to continue with the download: ").upper()
    if ok_continue == "OK":
        print("You will not see any console output until the downloads are complete. Stay patient :)")
        run_commands(cmds)


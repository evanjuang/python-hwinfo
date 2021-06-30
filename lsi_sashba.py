#!/usr/bin/env python3
import json
import glob
import shutil 
from subprocess import run, PIPE
from collections import OrderedDict


class LsiInfo():
    def __init__(self):
        self.lsi = OrderedDict()
        self.lsi['SAS3HBA'] = []

    def add_sas3hba(self, ctrl, vol, disk):
        ctrl['Volumes'] = vol
        ctrl['Disks'] = disk
        self.lsi['SAS3HBA'].append(ctrl)

    def to_json(self):
        return json.dumps(self.lsi)


def do_command(cmd):
    # print(cmd)
    result = run(cmd, shell=True, stdout=PIPE, stderr=PIPE)

    if result.returncode == 0:
        return result.stdout.decode()

    else:
        raise Exception('shell command:{}'.format(result.stderr.decode()))


def find_sd_name(sg):
    sd = glob.glob('/sys/block/sd*/device/scsi_generic/{}/'.format(sg))
    return sd[0].split('/')[3] if sd else ''


def find_devname_by_sn(sn):
    sg_vpd80 = glob.glob('/sys/class/scsi_generic/sg*/device/vpd_pg80')
    sg, sd = '', ''

    for _ in sg_vpd80:
        with open(_, 'rb') as fp:
            vpd_sn = bytearray(fp.read())[4:].decode()
            if sn in vpd_sn:
                sg = _.split('/')[-3]
                sd = find_sd_name(sg)
                break
    return sg, sd


def find_devname_by_sas_address(sas_address):
    sg_sas_address = glob.glob('/sys/class/scsi_generic/sg*/device/sas_address')
    sg, sd = '', ''

    for _ in sg_sas_address:
        with open(_, 'r') as fp:
            if sas_address in fp.read().strip():
                sg = _.split('/')[-3]
                sd = find_sd_name(sg)
                break
    return sg, sd


def parse_raw(raw):
    prop = OrderedDict()

    if not raw:
        return prop

    try:
        lines = filter(None, raw.split('\n'))

        for _ in lines:
            try:
                k, v = _.split(':', 1)
                if k and v:
                    v = v.strip()
                    prop[k.strip()] = int(v) if v.isdigit() else v
            except Exception:
                pass

    except Exception:
        pass

    return prop


class SAS3HBA():
    SAS3IRCU_CMD = "sas3ircu {} display | awk '/{}/,/-----/' | head -n -1"

    def __init__(self, ctrl_id):
        self.ctrl_id = ctrl_id

    def _ctrl_command(self):
        return self.SAS3IRCU_CMD.format(self.ctrl_id, 'Controller type')

    def _disk_command(self):
        return self.SAS3IRCU_CMD.format(self.ctrl_id, 'Device is a Hard disk')

    def _vol_command(self):
        return self.SAS3IRCU_CMD.format(self.ctrl_id, 'IR volume 1')

    def get_controller(self):
        raw = do_command(self._ctrl_command())
        return parse_raw(raw)

    def get_volume(self):
        def handle_phy_disk(prop):
            pd = []
            for k in [k for k in prop.keys() if k.startswith('PHY')]:
                e, s = prop.get(k).split(':')
                pd.append(OrderedDict([('Enclosure #', int(e)), ('Slot #', int(s))]))
                prop.pop(k, None)

            prop['PD'] = pd

        def find_devname(prop):
            wwid = prop.get('Volume wwid')
            prop['Device'] = ' '.join(find_devname_by_sas_address(wwid))

        volumes = []
        try:
            raw = do_command(self._vol_command())
            for _ in raw.split('IR volume'):
                if _:
                    vol_raw = _.split('\n', 1)[-1]
                    prop = parse_raw(vol_raw)
                    handle_phy_disk(prop)
                    find_devname(prop)
                    volumes.append(prop)

        except Exception:
            raise ValueError('parse volume data')

        return volumes

    def get_disk(self):
        def handle_size(prop):
            SIZE_KEY = 'Size (in MB)/(in sectors)'
            size = prop.get(SIZE_KEY)
            if size:
                mb, _ = size.split('/')
                prop['Size (in MB)'] = int(mb)
                prop.pop(SIZE_KEY, None)

        def find_devname(prop):
            sn = prop.get('Unit Serial No(VPD)')
            prop['Device'] = ' '.join(find_devname_by_sn(sn)).strip()

        disks = []
        try:
            raw = do_command(self._disk_command()).split('Device is a Hard disk')
            for _ in raw:
                if _:
                    prop = parse_raw(_)
                    handle_size(prop)
                    find_devname(prop)
                    disks.append(prop)

        except Exception:
            raise ValueError('parse disk data')

        return disks


def sas3hba_idx_list():
    CMD = 'sas3ircu list | egrep  \"\\b([[:xdigit:]]{2}h:){3}[[:xdigit:]]{2}h\\b\" | awk \'{print $1}\''
    try:
        raw = do_command(CMD)
        return filter(None, raw.split('\n'))

    except Exception:
        raise ValueError('scan HBA index')


def scan_sas3hba(lsi):
    for idx in sas3hba_idx_list():
        hba = SAS3HBA(idx)
        lsi.add_sas3hba(hba.get_controller(),
                        hba.get_volume(),
                        hba.get_disk())


if __name__ == "__main__":

    try:
        if not shutil.which('sas3ircu'):
            raise RuntimeError('sas3ircu not found!')

        lsi = LsiInfo()
        scan_sas3hba(lsi)

        print(lsi.to_json())


    except Exception as ex:
        print('ERROR: ' + str(ex))



#!/usr/bin/env python3

import os
import glob
import re


class ScsiHost():
    def __init__(self):
        self.name = None
        self.pci = None
        self.path = None
        self.slot = None
        self.ata_port = False
        self.end_device = []
        self.expander = []

    def __str__(self):
        return 'name={name},pci={pci},path={path}'.format(**self.__dict__)


class ScsiDevice():
    def __init__(self):
        self.model = None
        self.vendor = None
        self.sas_address = None
        self.block_name = None
        self.generic_name = None
        self.vpd80 = None

    def __str__(self):
        return 'model={model},vendor={vendor},sas_address={sas_address},'\
               'block_name={block_name},generic_name={generic_name},'\
               'vpd80={vpd80}'.format(**self.__dict__)


def read_attr(base, file_path):
    path = os.path.join(base, file_path)
    if os.path.isfile(path) and os.access(path, os.R_OK):
        try:
            with open(path, 'rb') as fp:
                data = fp.read().strip()
                try:
                    data = data.decode("utf-8")
                except UnicodeDecodeError:
                    pass
                return data
        except IOError:
            pass


def find_scsi_host():
    hosts = []
    for host in glob.glob('/sys/class/scsi_host/*'):
        h = ScsiHost()
        p = os.path.realpath(host)
        h.path = p
        h.name = p.rsplit('/', 1)[1]
        pci_bus = re.search('pci0000:00/(.+?)/host', p)
        if pci_bus:
            bus = pci_bus.group(1).split('/')
            if bus[-1].startswith('ata'):
                h.ata_port = bus[-1]
                h.pci = bus[:-1]
            else:
                h.pci = bus
        hosts.append(h)

    return hosts


def build_end_device(path):
    d = ScsiDevice()
    d.vendor = read_attr(path, 'vendor')
    d.model = read_attr(path, 'model')
    d.sas_address = read_attr(path, 'sas_address')

    block = glob.glob(os.path.join(path, 'block', 'sd*'))
    if block:
        d.block_name = os.path.basename(os.path.normpath(block[0]))

    generic = os.path.realpath(os.path.join(path, 'generic'))
    if generic:
        d.generic_name = os.path.basename(os.path.normpath(generic))

    return d


def discover_scsi_device(host):
    devices = []
    end_device = os.path.join(
        host.path, 'device', 'port-*', 'end_device-*'
    )

    expander_device = os.path.join(
        host.path, 'device', 'port-*', 'expander-*'
    )

    for device in glob.glob(end_device):
        target = glob.glob(os.path.join(device, 'target*', '*[0-9]'))

        if target:
            devices.append(build_end_device(target[0]))

    host.end_device = devices


def discover_pch_ata(host):
    ata_device_path = [os.path.realpath(_) for _ in glob.glob('/sys/class/scsi_disk/') if host.ata_port in os.path.realpath(_)]
    for device in ata_device_path:
        host.end_device.append(os.path.join(device, 'device'))


if __name__ == '__main__':
    hosts = find_scsi_host()
    for h in hosts:
        if h.ata_port:
            discover_pch_ata(h)
        else:
            discover_scsi_device(h)

        print(str(h))
        for d in h.end_device:
            print('\t' + str(d))

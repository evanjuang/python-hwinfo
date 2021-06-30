# python-hwinfo
Python scripts to get hardware information
## scsi.py
List scsi device
```
name=host0,pci=['0000:00:03.2', '0000:06:00.0'],path=/sys/devices/pci0000:00/0000:00:03.2/0000:06:00.0/host0/scsi_host/host0
        model=INTEL SSDSC2BA20,vendor=ATA,sas_address=0x4433221100000000,block_name=sda,generic_name=sg0,vpd80=None
        model=ST1200MM0007,vendor=SEAGATE,sas_address=0x5000c5008965d931,block_name=sdb,generic_name=sg1,vpd80=None
        model=ST1200MM0007,vendor=SEAGATE,sas_address=0x5000c5008965d365,block_name=sdc,generic_name=sg2,vpd80=None
name=host1,pci=['0000:00:11.4'],path=/sys/devices/pci0000:00/0000:00:11.4/ata1/host1/scsi_host/host1
name=host2,pci=['0000:00:11.4'],path=/sys/devices/pci0000:00/0000:00:11.4/ata2/host2/scsi_host/host2
name=host3,pci=['0000:00:11.4'],path=/sys/devices/pci0000:00/0000:00:11.4/ata3/host3/scsi_host/host3
name=host4,pci=['0000:00:11.4'],path=/sys/devices/pci0000:00/0000:00:11.4/ata4/host4/scsi_host/host4
name=host5,pci=['0000:00:1f.2'],path=/sys/devices/pci0000:00/0000:00:1f.2/ata5/host5/scsi_host/host5
name=host6,pci=['0000:00:1f.2'],path=/sys/devices/pci0000:00/0000:00:1f.2/ata6/host6/scsi_host/host6
name=host7,pci=['0000:00:1f.2'],path=/sys/devices/pci0000:00/0000:00:1f.2/ata7/host7/scsi_host/host7
name=host8,pci=['0000:00:1f.2'],path=/sys/devices/pci0000:00/0000:00:1f.2/ata8/host8/scsi_host/host8
name=host9,pci=['0000:00:1f.2'],path=/sys/devices/pci0000:00/0000:00:1f.2/ata9/host9/scsi_host/host9
name=host10,pci=['0000:00:1f.2'],path=/sys/devices/pci0000:00/0000:00:1f.2/ata10/host10/scsi_host/host10
```
## lsi_sashba.py
List Avago (LSI) SAS HBA, it requires `sas3ircu`.
```
{
    "SAS3HBA": [
        {
            "Controller type": "SAS3008",
            "PI Supported": "Yes",
            "PI Mixing": "Disabled",
            "BIOS version": "8.13.00.00",
            "Firmware version": "6.00.00.00",
            "Channel description": "1 Serial Attached SCSI",
            "Initiator ID": 0,
            "Maximum physical devices": 255,
            "Concurrent commands supported": 3072,
            "Slot": 1,
            "Segment": 0,
            "Bus": 6,
            "Device": 0,
            "Function": 0,
            "RAID Support": "Yes",
            "Volumes": [],
            "Disks": [
                {
                    "Enclosure #": 1,
                    "Slot #": 0,
                    "PI Supported": "No",
                    "SAS Address": "4433221-1-0000-0000",
                    "State": "Ready (RDY)",
                    "Manufacturer": "ATA",
                    "Model Number": "INTEL SSDSC2BA20",
                    "Firmware Revision": 140,
                    "Serial No": "BTHV546300DT200MGN",
                    "Unit Serial No(VPD)": "BTHV546300DT200MGN",
                    "GUID": "55cd2e404c13ecdd",
                    "Protocol": "SATA",
                    "Drive Type": "SATA_SSD",
                    "Size (in MB)": 190782,
                    "Device": "sg0 sda"
                },
                {
                    "Enclosure #": 1,
                    "Slot #": 2,
                    "PI Supported": "No",
                    "SAS Address": "5000c50-0-8965-d931",
                    "State": "Ready (RDY)",
                    "Manufacturer": "SEAGATE",
                    "Model Number": "ST1200MM0007",
                    "Firmware Revision": 2,
                    "Serial No": "S3L1QA0C",
                    "Unit Serial No(VPD)": "S3L1QA0C0000M54093KQ",
                    "GUID": "5000c5008965d933",
                    "Protocol": "SAS",
                    "Drive Type": "SAS_HDD",
                    "Size (in MB)": 1144641,
                    "Device": "sg1 sdb"
                },
                {
                    "Enclosure #": 1,
                    "Slot #": 4,
                    "PI Supported": "No",
                    "SAS Address": "5000c50-0-8965-d365",
                    "State": "Ready (RDY)",
                    "Manufacturer": "SEAGATE",
                    "Model Number": "ST1200MM0007",
                    "Firmware Revision": 2,
                    "Serial No": "S3L1LLF5",
                    "Unit Serial No(VPD)": "S3L1LLF50000M5360D34",
                    "GUID": "5000c5008965d367",
                    "Protocol": "SAS",
                    "Drive Type": "SAS_HDD",
                    "Size (in MB)": 1144641,
                    "Device": "sg2 sdc"
                }
            ]
        }
    ]
}
```

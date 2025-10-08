"""Example CLI outputs and TextFSM templates for CDP neighbor parsing.

This module provides example data for testing the TextFSM to TTP converter.
It includes both table-format (show cdp neighbors) and paragraph-format
(show cdp neighbors detail) examples along with their TextFSM templates
and target TTP template structures.
"""


class CDPExamples:
    # Table format example - show cdp neighbors
    TABLE_CLI_OUTPUT = """Capability Codes: R - Router, T - Trans Bridge, B- Source Route Bridge
           S - Switch, H - Host, I - IGMP, r - Repeater, P - Phone
Device ID         Local Intrfce Holdtme    Capability   Platform   Port ID
R1-PBX            Gig 1/0/10    144          R S I      2811       Fas 0/0
TS-1              Gig 1/0/39    122          R          2611       Eth 0/1
Cisco-WAP-N       Gig 1/0/1     120          T I        AIR-AP125  Gig 0
SEP04FE7F689D33   Gig 1/0/2     125          H P        IP Phone   Port 1
SEP000DBC50FCD1   Gig 1/0/4     147          H P        IP Phone   Port 1
SEP00124362C4D2   Gig 1/0/42    147          H P        IP Phone   Port 1"""

    TABLE_TEXTFSM = """Value Required NEIGHBOR_NAME (\S+)
Value LOCAL_INTERFACE (\S+(?:\s\S+)?)
Value CAPABILITIES ((?:\w\s)*\w)
Value PLATFORM ((?:[IiPp]{2}\s)?\S+)
Value NEIGHBOR_INTERFACE (.+?)

Start
  ^Device.*ID -> CDP
  # Capture time-stamp if vty line has command time-stamping turned on
  ^Load\s+for\s+
  ^Time\s+source\s+is

CDP
  ^${NEIGHBOR_NAME}$$
  ^\s*${LOCAL_INTERFACE}\s+\d+\s+${CAPABILITIES}\s+${PLATFORM}\s+${NEIGHBOR_INTERFACE}\s*$$ -> Record
  ^${NEIGHBOR_NAME}\s+${LOCAL_INTERFACE}\s+\d+\s+${CAPABILITIES}\s+${PLATFORM}\s+${NEIGHBOR_INTERFACE}\s*$$ -> Record"""

    # Paragraph format - show cdp neighbors detail
    DETAIL_CLI_OUTPUT = """Device ID: switchxxxxx
Entry address(es): 
  IP address: 1.1.1.1
Platform: cisco WS-C3560X-24P,  Capabilities: Switch IGMP 
Interface: GigabitEthernet0/3,  Port ID (outgoing port): GigabitEthernet0/8
Holdtime : 154 sec
Version :
Cisco IOS Software, C3560E Software (C3560E-UNIVERSALK9-M), Version 12.2(55)SE10, RELEASE SOFTWARE (fc2)
Technical Support: http://www.cisco.com/techsupport
Copyright (c) 1986-2015 by Cisco Systems, Inc.
Compiled Wed 11-Feb-15 11:28 by prod_rel_team
advertisement version: 2
Protocol Hello:  OUI=0x00000C, Protocol ID=0x0112; payload len=27, value=00000000FFFFFFFF010221FF00000000000000C88BC41880FF0000
VTP Management Domain: ''
Native VLAN: 1
Duplex: full
Power Available TLV:
    Power request id: 0, Power management id: 1, Power available: 0, Power management level: -1
Management address(es): 
  IP address: 1.1.1.1"""

    DETAIL_TEXTFSM = """Value Required NEIGHBOR_NAME (\S+)
Value MGMT_ADDRESS (\d+\.\d+\.\d+\.\d+|\w+\.\w+\.\w+)
Value PLATFORM (.*)
Value NEIGHBOR_INTERFACE (.*)
Value LOCAL_INTERFACE (.*)
Value NEIGHBOR_DESCRIPTION (.*$)
Value CAPABILITIES (.+?)

Start
  ^Device ID: ${NEIGHBOR_NAME}
  ^Entry address\(es\)\s*:\s* -> ParseIP
  ^Platform\s*:\s*${PLATFORM}\s*,\s*Capabilities\s*:\s*${CAPABILITIES}\s+$$
  ^Platform\s*:\s*${PLATFORM}\s*,\s*Capabilities\s*:\s*${CAPABILITIES}$$
  ^Interface: ${LOCAL_INTERFACE},  Port ID \(outgoing port\): ${NEIGHBOR_INTERFACE}
  ^Version : -> GetVersion
  # Capture time-stamp if vty line has command time-stamping turned on
  ^Load\s+for\s+
  ^Time\s+source\s+is

ParseIP
  ^.*IP address: ${MGMT_ADDRESS} -> Start
  ^Platform\s*:\s*${PLATFORM}\s*,\s*Capabilities\s*:\s*${CAPABILITIES}\s+$$ -> Start
  ^Platform\s*:\s*${PLATFORM}\s*,\s*Capabilities\s*:\s*${CAPABILITIES}$$ -> Start
  ^.* -> Start

GetVersion
  ^${NEIGHBOR_DESCRIPTION} -> Record Start"""

    # Example target TTP templates for reference
    TARGET_TTP_DETAIL = """Device ID: {{ device_id }}
  IP address: {{ ip_address | default('ip_not_found') }}
Platform: {{ platform | re(".*?(?=,)") }}, Capabilities: {{ capabilities | ORPHRASE }}
Interface: {{ local_interface }},  Port ID (outgoing port): {{ remote_interface }}"""

    # TTP template for table format
    TABLE_TTP = """
<group name="neighbors">
{{neighbor}}       {{ local_interface | ORPHRASE }}     {{ hold_time | isdigit }}          {{ capabilities | ORPHRASE }}        {{ platform }}  {{ remote_interface | ORPHRASE}}
</group>"""

    # The paragraph format TTP template we can keep from your existing TARGET_TTP_DETAIL:
    DETAIL_TTP = """Device ID: {{ device_id }}
  IP address: {{ ip_address | default('ip_not_found') }}
Platform: {{ platform | re(".*?(?=,)") }}, Capabilities: {{ capabilities | ORPHRASE }}
Interface: {{ local_interface }},  Port ID (outgoing port): {{ remote_interface }}"""

    @classmethod
    def get_example(self, cls, example_type: str, template_type: str) -> tuple[str, str]:
        """Get example CLI output and matching template.

        Args:
            example_type: Format of CDP output - either 'table' or 'detail'
            template_type: Parser type - either 'textfsm' or 'ttp'

        Returns:
            tuple: (cli_output, template)
        """
        if example_type == 'table':
            cli_output = cls.TABLE_CLI_OUTPUT
            template = cls.TABLE_TEXTFSM if template_type == 'textfsm' else cls.TABLE_TTP
        else:  # detail
            cli_output = cls.DETAIL_CLI_OUTPUT
            template = cls.DETAIL_TEXTFSM if template_type == 'textfsm' else cls.DETAIL_TTP

        return cli_output, template
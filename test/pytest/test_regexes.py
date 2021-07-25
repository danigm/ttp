import sys

sys.path.insert(0, "../..")
import pprint

import logging

logging.basicConfig(level="INFO")

from ttp import ttp


def test_pipe_separated_regexes():
    template = """
<input load="text">
Protocol  Address     Age (min)  Hardware Addr   Type   Interface
Internet  10.12.13.1        98   0950.5785.5cd1  ARPA   FastEthernet2.13
Internet  10.12.13.2        98   0950.5785.5cd2  ARPA   Loopback0
Internet  10.12.13.3       131   0150.7685.14d5  ARPA   GigabitEthernet2.13
Internet  10.12.13.4       198   0950.5C8A.5c41  ARPA   GigabitEthernet2.17
</input>

<vars>
INTF_RE = r"GigabitEthernet\\S+|Fast\\S+"
</vars>

<group name="arp_test">
Internet  {{ ip | re("IP")}}  {{ age | re(r"\\d+") }}   {{ mac }}  ARPA   {{ interface | re("INTF_RE") }}
</group>
"""
    parser = ttp(template=template)
    parser.parse()
    res = parser.result()
    # pprint.pprint(res)
    assert res == [
        [
            {
                "arp_test": [
                    {
                        "age": "98",
                        "interface": "FastEthernet2.13",
                        "ip": "10.12.13.1",
                        "mac": "0950.5785.5cd1",
                    },
                    {
                        "age": "131",
                        "interface": "GigabitEthernet2.13",
                        "ip": "10.12.13.3",
                        "mac": "0150.7685.14d5",
                    },
                    {
                        "age": "198",
                        "interface": "GigabitEthernet2.17",
                        "ip": "10.12.13.4",
                        "mac": "0950.5C8A.5c41",
                    },
                ]
            }
        ]
    ]


# test_pipe_separated_regexes()


def test_multiple_inline_regexes():
    template = """
<input load="text">
Protocol  Address     Age (min)  Hardware Addr   Type   Interface
Internet  10.12.13.1        98   0950.5785.5cd1  ARPA   FastEthernet2.13
Internet  10.12.13.2        98   0950.5785.5cd2  ARPA   Loopback0
Internet  10.12.13.3       131   0150.7685.14d5  ARPA   GigabitEthernet2.13
Internet  10.12.13.4       198   0950.5C8A.5c41  ARPA   GigabitEthernet2.17
</input>

<vars>
INTF_RE = r"GigabitEthernet\\S+|Fast\\S+"
</vars>

<group name="arp_test">
Internet  {{ ip }}  {{ age }}   {{ mac }}  ARPA   {{ interface | re(r"GigabitEthernet\\S+") | re(r"Fast\\S+") }}
</group>
"""
    parser = ttp(template=template)
    parser.parse()
    res = parser.result()
    # pprint.pprint(res)
    assert res == [
        [
            {
                "arp_test": [
                    {
                        "age": "98",
                        "interface": "FastEthernet2.13",
                        "ip": "10.12.13.1",
                        "mac": "0950.5785.5cd1",
                    },
                    {
                        "age": "131",
                        "interface": "GigabitEthernet2.13",
                        "ip": "10.12.13.3",
                        "mac": "0150.7685.14d5",
                    },
                    {
                        "age": "198",
                        "interface": "GigabitEthernet2.17",
                        "ip": "10.12.13.4",
                        "mac": "0950.5C8A.5c41",
                    },
                ]
            }
        ]
    ]


# test_multiple_inline_regexes()

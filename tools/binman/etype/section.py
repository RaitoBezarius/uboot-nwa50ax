# SPDX-License-Identifier:      GPL-2.0+
# Copyright (c) 2018 Google, Inc
# Written by Simon Glass <sjg@chromium.org>
#
# Entry-type module for sections, which are entries which can contain other
# entries.
#

from entry import Entry
import fdt_util
import tools

import bsection

class Entry_section(Entry):
    def __init__(self, image, etype, node):
        Entry.__init__(self, image, etype, node)
        self._section = bsection.Section(node.name, node)

    def ProcessFdt(self, fdt):
        return self._section.ProcessFdt(fdt)

    def AddMissingProperties(self):
        Entry.AddMissingProperties(self)
        self._section.AddMissingProperties()

    def ObtainContents(self):
        return self._section.GetEntryContents()

    def GetData(self):
        return self._section.GetData()

    def GetOffsets(self):
        """Handle entries that want to set the offset/size of other entries

        This calls each entry's GetOffsets() method. If it returns a list
        of entries to update, it updates them.
        """
        self._section.GetEntryOffsets()
        return {}

    def Pack(self, offset):
        """Pack all entries into the section"""
        self._section.PackEntries()
        self.size = self._section.CheckSize()
        return super(Entry_section, self).Pack(offset)

    def WriteSymbols(self, section):
        """Write symbol values into binary files for access at run time"""
        self._section.WriteSymbols()

    def SetCalculatedProperties(self):
        Entry.SetCalculatedProperties(self)
        self._section.SetCalculatedProperties()

    def ProcessContents(self):
        self._section.ProcessEntryContents()
        super(Entry_section, self).ProcessContents()

    def CheckOffset(self):
        self._section.CheckEntries()

    def WriteMap(self, fd, indent):
        """Write a map of the section to a .map file

        Args:
            fd: File to write the map to
        """
        super(Entry_section, self).WriteMap(fd, indent)
        self._section.WriteMap(fd, indent + 1)

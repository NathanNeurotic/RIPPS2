<@986969041161830440> we were snooping about on psx-place and saw your note that the APA structure is bound to the disk's size, and that a disk image written to a drive of another size corrupts the chain as more partitions get made. We wanted to double check from your guidance before build 114 touches it.

114 adds deleting a game completely. On an APA drive that removes the game's PP. partition through the driver's own remove (RIPPS2 never creates partitions, and its driver refuses creates). Before any partition goes, RIPPS2 will walk the whole chain read only and refuse if anything does not fit this disk:
- every header's magic and checksum, each next and prev pointing at each other, and the chain closing back at __mbr
- every partition inside the disk's real sector count
- no partition larger than this disk allows, and none off its power of two alignment
The same walk runs again after the delete, and the HDD Manager's remove gets the same check.

Is there a check you would add, or a case where removing a partition on a cloned table is still unsafe?

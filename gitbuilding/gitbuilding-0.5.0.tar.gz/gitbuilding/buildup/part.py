'''
This submodule contains functionality to handle parts in the BuildUp documentation.
It contains the Part and PartList classes.
'''

from copy import copy
import logging
from gitbuilding.buildup.quantity import Quantity, largest_quantity

_LOGGER = logging.getLogger('BuildUp')

class Part:
    """
    This class represents a particular part such as "M3x6mm Cap Head Screws".
    It handles counting the quantity of the part used, its category, and notes
    about usage etc.

    Part objects which are included in a partlist are "indexed"
    Part objects which are not are not "indexed" this definition is important as it
    affects how parts are compared. For example, when comparing two indexed parts they
    will are both already on PartLists (i.e. lists for different pages), so all
    information must agree for them to be equal. Comparing an indexed part to an
    un-indexed part happens when a new part is found on a page, if only the name matches
    (and no link is defined) then this is a reuse of the same part.
    """

    BOTH_INDEXED = 2
    ONE_INDEXED = 1

    def __init__(self, link, doc, indexed=False):

        self._doc = doc
        self._valid = True
        # An indexed part is one that has been added to a partlist
        self._indexed = indexed
        self._link = link
        self._cat = self._doc.config.default_category
        self._reuse = False
        # None for total quantity would mean that no total is defined and it is
        # calculated from number used
        self._total_qty = None
        # qty_used is set as None because type has not yet been set
        self._qty_used = None
        self._note = None

        self._construct_part()

    @property
    def valid(self):
        """
        Read-only property. Returns whether the Part is valid.
        """
        return self._valid

    @property
    def indexed(self):
        """
        Read only property that returns whether the part is indexed.
        An indexed part is a part that is in a part list. A non-indexed
        part is a part that is yet to be added to a list. This distinction
        is important when comparing parts.
        """
        return self._indexed

    def set_indexed(self, indexed):
        """
        Sets whether part has been indexed onto a partlist
        """
        self._indexed = indexed

    @property
    def name(self):
        """
        Read-only property: The name of the part. This is equivalent to
        the text of the link in the build up.
        """
        return self.link.linktext

    @property
    def link(self):
        """
        Read-only property: The link object that created the part
        """
        return self._link

    @property
    def linklocation(self):
        """
        Read-only property: The URL for the part relative to the root of the
        directory
        """
        if self.link.link_rel_to_root == '':
            return None
        return self.link.link_rel_to_root

    @property
    def cat(self):
        """
        Read-only property: The category of the part.
        """
        return self._cat

    @property
    def total_qty(self):
        """
        Read-only property: The total quantity of the part used in the
        partlist it is indexed in.
        """
        return self._total_qty

    @property
    def qty_used(self):
        """
        Read-only property: The total quantity of this used in this part list
        as counted on this page. Does not have much meaning for aggregate lists
        This differs from total_qty as total_qty can be set explicitly where as
        this is directly as counted from the page. If total_qty is not set then
        total_qty will be set equal to qty_used when `set_total` is run. If
        total_qty is set and doesn't match qty_used when `set_total` is run, a
        warning will be logged.
        """
        return self._qty_used

    @property
    def note(self):
        """
        Read-only property: this returns any notes defined for the part
        """
        return self._note

    def _set_total_qty(self, part_info):
        # if Qty not defined or set as ?, leave qty as None
        if "totalqty" in part_info:
            total_qty = Quantity(part_info["totalqty"])
            if total_qty.valid:
                self._total_qty = total_qty
            else:
                _LOGGER.warning('Could not parse the quantity "%s"', part_info["totalqty"])
            del part_info["totalqty"]

    def _set_cat(self, part_info):
        if "cat" in part_info:
            if part_info["cat"].lower() in self._doc.config.categories:
                self._cat = part_info["cat"].lower()
                self._reuse = self._doc.config.categories[self._cat].reuse
            else:
                _LOGGER.warning("No valid category %s. You can define custom categories"
                                " in the config file.",
                                part_info['cat'])
            del part_info["cat"]

    def _set_note(self, part_info):
        if "note" in part_info:
            if isinstance(part_info["note"], str):
                self._note = part_info["note"]
            else:
                _LOGGER.warning("Ignoring the Note '%s' I expected a string not a %s.",
                                part_info['note'], type(part_info['note']))
            del part_info["note"]


    def _construct_part(self):
        """
        Strips the important part information from the data in a buildup file
        """

        part_info = self.link.build_up_dict
        if part_info is None:
            self._valid = False
            return

        # An indexed part is from a part defined in a link reference
        # A non-indexed one is from an inline part link
        if self._indexed:
            # read keys from a link reference
            self._set_total_qty(part_info)
            self._set_cat(part_info)
            self._set_note(part_info)
        else:
            # read keys from an inline part link
            if "qty" in part_info:
                qty_used = Quantity(part_info["qty"])
                if qty_used.valid:
                    self._qty_used = qty_used
                else:
                    self._valid = False
                    _LOGGER.warning('Could not parse the quantity "%s"', part_info["qty"])
            else:
                self._valid = False
                _LOGGER.warning("Part link without quantity [%s]. This will be ignored",
                                {self.name})
                return
            del part_info["qty"]

        if len(part_info.keys()) > 0:
            keynames = ""
            for key in part_info:
                keynames += key + ", "
            _LOGGER.warning("Unused keys '%s' in part [%s]",
                            keynames[:-2],
                            self.name,
                            extra={'fussy':True})

    def _both_indexed_eq(self, obj):
        # Comparing two parts already in parts lists on different
        # pages of the documentation.

        # categories must match
        if self._cat != obj.cat:
            return False

        # If either link is None just check name.
        if (self.linklocation is None) or (obj.linklocation is None):
            if self.name == obj.name:
                if self.linklocation != obj.linklocation:
                    if self.linklocation is None:
                        link = obj.linklocation
                    else:
                        link = self.linklocation
                    _LOGGER.warning("Two parts have same name '%s' but the link is"
                                    " undefined for one of them. Using %s for both in"
                                    " combined Bill of Materials.",
                                    obj.name,
                                    link,
                                    fussy=True)
                return True
            return False

        # If links match then they are referring to the same part
        if self.linklocation == obj.linklocation:
            if self.name != obj.name:
                _LOGGER.warning("Two parts have same link '%s' and different names [%s, %s]."
                                " One name will be picked for the combined Bill of Materials.",
                                obj.linklocation,
                                self.name,
                                obj.name,
                                extra={'fussy':True})
            return True
        return False

    def _one_indexed_eq(self, obj):
        # Non indexed part compared to an indexed one.
        # This will be for checking whether to increment the parts used or to
        # index the part as a new part
        # Categories don't need to match here as using "qty" for a part
        # to be counted shouldn't set the category

        if self.name != obj.name:
            # names must match
            return False

        if self.linklocation == obj.linklocation:
            # categories, names and links match
            return True

        if obj.linklocation is None or self.linklocation is None:
            return True

        _LOGGER.warning("Parts on same page have the same name: '%s'"
                        " and different links [%s, %s]. "
                        "This may cause weird Bill of Materials issues.",
                        obj.name,
                        self.linklocation,
                        obj.linklocation)
        return False

    def __eq__(self, obj):
        """
        Checks is two parts are equal.
        This one is somewhat weird as it depends on what is being compared:
        * String input checks the name.
        * If both parts are indexed (i.e. on part lists) then they are from different
          pages in the documentation. These need to be checked carefully to avoid clashes
          between parts on different pages in a total Bill of Materials
        * If only one part is indexed (on a part list) then the check is within a page
        More details about how the checks are done is in the comments of the function
        """

        if isinstance(obj, str):
            return obj == self.name
        if isinstance(obj, Part):
            # Check type depends on if an indexed part (one in a PartList) is
            # compared to another indexed part or one not yet indexed (see
            # below)
            check_type = self._indexed + obj.indexed
            if check_type not in [self.BOTH_INDEXED, self.ONE_INDEXED]:
                raise RuntimeError("Part comparison failed, are you trying to compare"
                                   " two non-indexed Parts?")

            if check_type == self.ONE_INDEXED:
                return self._one_indexed_eq(obj)
            return self._both_indexed_eq(obj)
        return False

    def __str__(self):
        return (f"{self.name:}\n"
                "link:      {self._link}\n"
                "category:  {self._cat}\n"
                "reuse:     {self._reuse}\n"
                "Total Qty: {self._total_qty}\n"
                "Qty Used:  {self._qty_used}\n")


    def combine(self, part):
        """
        Combines two parts of the same part
        Combine is different from counting, combine is the operation when two lists are merged
        as such all parts should be indexed (i.e. on parts lists)
        """

        if not isinstance(part, Part):
            raise TypeError("Can only add a Part to a Part")
        if not (self._indexed and part.indexed):
            raise RuntimeError("Can only combine two indexed parts")
        if part != self:
            raise RuntimeError("Parts must match to be combines")

        if self._reuse:
            self._qty_used = largest_quantity(self._qty_used, part.qty_used)
        else:
            self._qty_used = self._qty_used + part.qty_used

        if self._reuse:
            self._total_qty = largest_quantity(self._total_qty, part.total_qty)
        else:
            self._total_qty = self._total_qty + part.total_qty

        if self._note is None:
            self._note = part.note
        elif part.note is not None:
            self._note += "  " + part.note

    def count(self, part):
        """
        Counts more of the same part on a page. This is not used when merging two lists of parts
        for merging lists see combine
        """

        if not self._indexed:
            raise RuntimeError("Only indexed parts can count other parts")
        if part.indexed:
            raise RuntimeError("Can only count non indexed parts")

        if self._qty_used is None:
            self._qty_used = part.qty_used
        else:
            if self._reuse:
                self._qty_used = largest_quantity(self._qty_used, part.qty_used)
            else:
                self._qty_used = self._qty_used + part.qty_used

    def set_total(self):
        """
        If total is not already set it sets it to the quantity used.
        """
        if self._total_qty is None:
            self._total_qty = self._qty_used

    def bom_line(self):
        '''
        Writes the markdown line for the bill of materials
        '''
        appended_class = ""
        if self._total_qty is None:
            return ""
        if isinstance(self._total_qty, int):
            qty_str = str(self._total_qty) + " x "
        elif isinstance(self._total_qty, float):
            qty_str = str(self._total_qty) + " of "
        else:
            qty_str = str(self.total_qty)

        if self.linklocation is None:
            appended_class = '{: Class="missing"}'

        if self._note is None:
            note_txt = ""
        else:
            note_txt = "  " + self._note
        return f"* {qty_str} [{self.name}]{appended_class} {note_txt}\n"

class PartList:
    """
    PartLists are lists of Part objects. They have functions that allow them to
    safely add parts and to be merged.
    Lists start of not "counted". Once all parts in a page have been added into the list
      it can be "counted" to create total quantities for each part
    Lists can also be created as Aggregate lists, these are used to merge multiple lists
      together for making total bills of materials.
    The main reasons for this distinction is so that the software can separate information
    that is assumed from information that is read. Assumptions are then made when the list
    is counted.
    """

    def __init__(self, doc, AggregateList=False):
        # aggregate lists are summed lists, a non aggregate list cannot become
        # an aggregate
        self._aggregate = AggregateList
        # All aggregate lists are counted, normal lists should be counted before
        # merging into aggregates or calculating a bill of materials
        self._counted = AggregateList
        self._parts = []
        self._doc = doc

    @property
    def counted(self):
        """
        Read only property which denotes whether the list is counted.
        To count a list run `finished_counting` this will count the
        total quantities of all parts in the list. Allowing merging
        and calculating bills of materials. Once a list is counted
        you can no longer use count_part.
        """
        return self._counted

    def __getitem__(self, ind):
        return self._parts[ind]

    def __setitem__(self, ind, part):
        if not isinstance(part, Part):
            raise TypeError("Can only store Part objects in a PartList")
        self._parts[ind] = part

    def __len__(self):
        return len(self._parts)

    def append(self, part):
        """
        Appends a new part into the list, this is done for parts defined by reference
        links. For parts in the page count_part is used, this will append the part if
        it is not already defined.
        """

        if not isinstance(part, Part):
            raise TypeError("Can only append Part objects to a PartList")
        if not part.indexed:
            raise RuntimeError("Can only append indexed parts objects to a PartList")

        # If there was an error the part data then the part is not valid and wont be
        # appended
        if part.valid:
            self._parts.append(copy(part))

    def index(self, part):
        """
        Works as index for a list but uses the __eq__ method of Part objects
        in the part list
        """
        return self._parts.index(part)

    def getpart(self, part):
        """
        Returns the part object from the list that matches input "part"
        uses the __eq__ method of Parts, so this input could be a Part
        object or a string
        """
        if part in self._parts:
            return self._parts[self.index(part)]
        return None

    def merge(self, inputlist):
        """
        If this is an aggregate list then it merges in another partlist
        """
        if not isinstance(inputlist, PartList):
            raise TypeError("Can only merge a PartList to another PartList")
        if not self._aggregate:
            raise RuntimeError("Only aggregate lists can merge other lists into them")
        if not inputlist.counted:
            raise RuntimeError("List must be counted before being merged into an aggregate")
        for part in inputlist:
            if part in self:
                ind = self._parts.index(part)
                self[ind].combine(part)
            else:
                self.append(part)

    def count_part(self, part):
        """
        Takes the information for another part and counts it.
        If the part already exists then counting rules are used to add the quantities
        If it doesn't exist we append it
        """
        if self._counted:
            raise RuntimeError("Cannot count part, counting has finished")
        if part.indexed:
            raise RuntimeError("Cannot count an indexed part")

        if part.valid:
            # if the part is already listed, update quantities
            if part in self._parts:
                ind = self._parts.index(part)
                self[ind].count(part)
            else:
                part.set_indexed(True)
                self.append(part)

    def finish_counting(self):
        """
        Calculates the total quantities for each part on the list and
        then marks the list as "counted"
        """
        if self._counted:
            return
        # once counting is finished, if the total quantity was undefined set it
        # to the quantity used
        for part in self._parts:
            part.set_total()
            if part.total_qty != part.qty_used:
                _LOGGER.warning("%s has a total quantity of %s specified but only %s are used.",
                                part.name,
                                part.total_qty,
                                part.qty_used,
                                extra={'fussy':True})
        self._counted = True

    def link_refs_md(self, url_translator, excludelist=None):
        """
        Returns the markdown down for the links to each part. Each part on a new line
        """
        linktext = ""

        if excludelist is None:
            excludelist = []

        for part in self._parts:
            if part not in excludelist:
                linktext += f"{part.link.link_ref_md(url_translator)}\n"
        return linktext

    def bom_md(self, title, url_translator, divide=True, exclude_refs=None):
        """
        Creates the bill of materials in markdown format.
        Can set whether it also includes the link references for each
        part, and whether they are divided by categories
        """

        if not self._counted:
            raise RuntimeError("Cannot calculate bill of materials for uncounted partlist.")
        bom_text = ""
        if title != "":
            bom_text += f"{title}\n\n"
        # Loop through parts and put quantities and names in/
        if divide:
            for cat in self._doc.config.categories:
                catname = self._doc.config.categories[cat].display_name
                first = True
                for part in self._parts:
                    if part.cat == cat:
                        if first:
                            first = False
                            bom_text += f"\n\n### {catname}\n\n"

                        bom_text += part.bom_line()
        else:
            for part in self._parts:
                bom_text += part.bom_line()
        bom_text += self.link_refs_md(url_translator, exclude_refs)
        bom_text += "\n\n"
        return bom_text
